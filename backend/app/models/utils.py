from typing import Tuple, Optional, List
import cv2
import numpy as np
import torch
import logging

from ..config import settings, IMAGENET_MEAN, IMAGENET_STD

logger = logging.getLogger(__name__)

# Lazy import for face detection (only load when needed)
_face_detector = None


def normalize_lighting(img_bgr: np.ndarray, clip_limit: float = 2.0, tile_size: int = 8) -> np.ndarray:
	"""
	Normalize lighting using CLAHE on luminance to handle dramatic highlights/shadows,
	indoor lighting, and warm tones. Makes face detection and model input more consistent.
	
	Args:
		img_bgr: BGR image
		clip_limit: CLAHE contrast limit (higher = more aggressive)
		tile_size: Grid size for adaptive histogram
	
	Returns:
		BGR image with normalized lighting
	"""
	lab = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2LAB)
	L, a, b = cv2.split(lab)
	clahe = cv2.createCLAHE(clipLimit=clip_limit, tileGridSize=(tile_size, tile_size))
	L_norm = clahe.apply(L)
	lab_norm = cv2.merge([L_norm, a, b])
	return cv2.cvtColor(lab_norm, cv2.COLOR_LAB2BGR)


def _get_face_detector():
	"""Lazy load MTCNN face detector to avoid loading on import."""
	global _face_detector
	if _face_detector is None:
		try:
			from mtcnn import MTCNN
			# MTCNN initialization - correct parameter names
			_face_detector = MTCNN(
				min_face_size=20,
				steps_threshold=[0.6, 0.7, 0.7],
				scale_factor=0.709
			)
			logger.info("MTCNN face detector initialized")
		except ImportError:
			logger.warning("MTCNN not available. Install with: pip install mtcnn")
			_face_detector = False  # Mark as unavailable
		except Exception as e:
			logger.warning(f"Failed to initialize MTCNN: {e}")
			_face_detector = False  # Mark as unavailable
	return _face_detector


def load_image_bgr(path: str) -> np.ndarray:
	"""Load image in BGR format using OpenCV."""
	img = cv2.imread(path, cv2.IMREAD_COLOR)
	if img is None:
		raise ValueError(f"Failed to read image: {path}")
	return img


def detect_faces(img_rgb: np.ndarray, min_face_size: int = 64, confidence: float = 0.9) -> List[dict]:
	"""
	Detect faces in an RGB image using MTCNN.
	
	Args:
		img_rgb: RGB image as numpy array (H, W, 3)
		min_face_size: Minimum face size in pixels
		confidence: Minimum confidence threshold for face detection
	
	Returns:
		List of detected faces, each containing:
		- 'box': [x, y, width, height]
		- 'confidence': detection confidence
		- 'keypoints': facial landmarks (optional)
	"""
	detector = _get_face_detector()
	if detector is False or detector is None:
		return []
	
	try:
		faces = detector.detect_faces(img_rgb)
		# Filter by confidence and size
		filtered_faces = []
		for face in faces:
			if face['confidence'] >= confidence:
				x, y, w, h = face['box']
				face_size = min(w, h)
				if face_size >= min_face_size:
					filtered_faces.append(face)
		return filtered_faces
	except Exception as e:
		logger.warning(f"Face detection failed: {e}")
		return []


def extract_face_region(img_rgb: np.ndarray, face_box: dict, padding: float = 0.2) -> np.ndarray:
	"""
	Extract and crop face region from image with padding.
	
	Args:
		img_rgb: RGB image as numpy array
		face_box: Face detection result with 'box' key [x, y, width, height]
		padding: Padding ratio around face (0.2 = 20% padding)
	
	Returns:
		Cropped face region as RGB image
	"""
	x, y, w, h = face_box['box']
	img_h, img_w = img_rgb.shape[:2]
	
	# Calculate padding
	padding_x = int(w * padding)
	padding_y = int(h * padding)
	
	# Calculate crop coordinates with bounds checking
	x1 = max(0, x - padding_x)
	y1 = max(0, y - padding_y)
	x2 = min(img_w, x + w + padding_x)
	y2 = min(img_h, y + h + padding_y)
	
	# Extract face region
	face_crop = img_rgb[y1:y2, x1:x2]
	return face_crop


def detect_and_extract_largest_face(img_rgb: np.ndarray, min_face_size: int = 64, 
								   confidence: float = 0.85, padding: float = 0.2,
								   retry_lower_confidence: bool = True) -> Optional[np.ndarray]:
	"""
	Detect faces and extract the largest face region. Retries with lower confidence
	if no face found (helps with dramatic lighting, indoor, warm tones).
	
	Args:
		img_rgb: RGB image as numpy array
		min_face_size: Minimum face size in pixels
		confidence: Minimum confidence threshold
		padding: Padding ratio around face
		retry_lower_confidence: If True, retry with 0.75 then 0.6 when no face found
	
	Returns:
		Cropped face region as RGB image, or None if no face detected
	"""
	confidences = [confidence]
	if retry_lower_confidence and confidence > 0.6:
		if confidence > 0.75:
			confidences.append(0.75)
		if confidence > 0.6:
			confidences.append(0.6)
	
	for conf in confidences:
		faces = detect_faces(img_rgb, min_face_size, conf)
		if faces:
			# Select largest face (by area)
			largest_face = max(faces, key=lambda f: f['box'][2] * f['box'][3])
			face_crop = extract_face_region(img_rgb, largest_face, padding)
			if conf < confidence:
				logger.debug(f"Face detected with fallback confidence {conf}")
			return face_crop
	
	return None


def preprocess_image_for_model(img_bgr: np.ndarray, size: Tuple[int, int] | None = None,
							   use_face_detection: bool = True, min_face_size: int = 64,
							   face_confidence: float = 0.85, face_padding: float = 0.2,
							   use_lighting_normalization: bool = True,
							   use_imagenet_normalization: bool = True) -> torch.Tensor:
	"""
	Preprocess image for model input (ResNet expects 224x224, ImageNet-normalized).
	
	Args:
		img_bgr: BGR image as numpy array
		size: Target size (default 224x224 for ResNet)
		use_face_detection: Whether to detect and extract face first
		min_face_size: Minimum face size for detection
		face_confidence: Face detection confidence threshold
		face_padding: Padding ratio around detected face
		use_lighting_normalization: CLAHE before face detection for challenging lighting
		use_imagenet_normalization: Apply ImageNet mean/std (required for ResNet)
	
	Returns:
		Preprocessed tensor (3, H, W), ImageNet-normalized if use_imagenet_normalization
	"""
	if size is None:
		s = settings.MODEL_INPUT_SIZE
		size = (s, s)
	# Lighting normalization first - helps face detection in dramatic/indoor/warm lighting
	if use_lighting_normalization:
		img_bgr = normalize_lighting(img_bgr)
	
	# Convert BGR to RGB
	img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
	
	# Face detection and extraction
	if use_face_detection:
		face_crop = detect_and_extract_largest_face(
			img_rgb, 
			min_face_size=min_face_size,
			confidence=face_confidence,
			padding=face_padding
		)
		if face_crop is not None:
			img_rgb = face_crop
			logger.debug("Face detected and extracted")
		else:
			logger.warning("No face detected, using full image")
	
	# Resize to target size
	img_resized = cv2.resize(img_rgb, size, interpolation=cv2.INTER_AREA)
	
	# Normalize to [0, 1]
	img_normalized = img_resized.astype(np.float32) / 255.0
	
	# Convert HWC to CHW
	img_tensor = np.transpose(img_normalized, (2, 0, 1))
	tensor = torch.from_numpy(img_tensor).float()

	# ImageNet normalization for pretrained ResNet
	if use_imagenet_normalization:
		mean = torch.tensor(IMAGENET_MEAN).view(3, 1, 1)
		std = torch.tensor(IMAGENET_STD).view(3, 1, 1)
		tensor = (tensor - mean) / std

	return tensor
















