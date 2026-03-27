from pathlib import Path
from typing import Dict, Any, List, Tuple
import numpy as np
import cv2
import torch
import logging

from ..models.detector import load_detector, predict_image
from ..models.utils import load_image_bgr, preprocess_image_for_model
from ..config import settings
from .heatmap import save_dummy_heatmap

logger = logging.getLogger(__name__)


def run_image_inference(image_path: Path) -> Dict[str, Any]:
	"""Run inference on a single image with face detection preprocessing."""
	model = load_detector()
	img = load_image_bgr(str(image_path))
	
	# Preprocess with face detection and lighting normalization (224x224, ImageNet norm for ResNet)
	tensor = preprocess_image_for_model(
		img,
		use_face_detection=settings.USE_FACE_DETECTION,
		min_face_size=settings.MIN_FACE_SIZE,
		face_confidence=settings.FACE_DETECTION_CONFIDENCE,
		face_padding=settings.FACE_PADDING,
		use_lighting_normalization=settings.USE_LIGHTING_NORMALIZATION
	)
	
	if torch.cuda.is_available():
		tensor = tensor.to("cuda")
	
	score, label = predict_image(
		model, tensor,
		uncertain_low=settings.UNCERTAIN_LOW,
		uncertain_high=settings.UNCERTAIN_HIGH
	)
	heatmap_path = save_dummy_heatmap(image_path, score)
	
	return {
		"score": float(score),
		"label": label,
		"heatmap_path": str(heatmap_path),
		"face_detected": settings.USE_FACE_DETECTION  # Indicate if face detection was used
	}


def extract_video_frames(video_path: Path, out_dir: Path, max_frames: int = 64) -> List[Path]:
	out_dir.mkdir(parents=True, exist_ok=True)
	cap = cv2.VideoCapture(str(video_path))
	count = 0
	frame_paths: List[Path] = []
	success, frame = cap.read()
	while success and count < max_frames:
		filename = out_dir / f"frame_{count:04d}.png"
		cv2.imwrite(str(filename), frame)
		frame_paths.append(filename)
		count += 1
		success, frame = cap.read()
	cap.release()
	return frame_paths


def run_video_inference(frame_paths: List[Path]) -> Tuple[float, str, List[float]]:
	"""Run inference on video frames with face detection preprocessing."""
	model = load_detector()
	per_frame_scores: List[float] = []
	device = torch.device("cuda") if torch.cuda.is_available() else torch.device("cpu")
	model.to(device)
	
	faces_detected_count = 0
	
	for frame_path in frame_paths:
		try:
			img = load_image_bgr(str(frame_path))
			# Preprocess with face detection and lighting normalization
			tensor = preprocess_image_for_model(
				img,
				use_face_detection=settings.USE_FACE_DETECTION,
				min_face_size=settings.MIN_FACE_SIZE,
				face_confidence=settings.FACE_DETECTION_CONFIDENCE,
				face_padding=settings.FACE_PADDING,
				use_lighting_normalization=settings.USE_LIGHTING_NORMALIZATION
			)
			tensor = tensor.to(device)
			score, _ = predict_image(
				model, tensor,
				uncertain_low=settings.UNCERTAIN_LOW,
				uncertain_high=settings.UNCERTAIN_HIGH
			)
			per_frame_scores.append(float(score))
			
			# Check if face was detected (rough heuristic: if preprocessing worked)
			if settings.USE_FACE_DETECTION:
				faces_detected_count += 1
		except Exception as e:
			logger.warning(f"Failed to process frame {frame_path}: {e}")
			# Skip failed frames
			continue
	
	if len(per_frame_scores) == 0:
		return 0.0, "REAL", per_frame_scores
	
	avg_score = float(np.mean(per_frame_scores))
	if avg_score < settings.UNCERTAIN_LOW:
		label = "REAL"
	elif avg_score >= settings.UNCERTAIN_HIGH:
		label = "FAKE"
	else:
		label = "UNCERTAIN"
	
	logger.info(f"Processed {len(per_frame_scores)}/{len(frame_paths)} frames, "
			   f"faces detected in {faces_detected_count} frames")
	
	return avg_score, label, per_frame_scores
















