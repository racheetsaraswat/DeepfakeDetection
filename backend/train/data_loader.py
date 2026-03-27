from pathlib import Path
from typing import Tuple, List, Optional
import random
import torch
from torch.utils.data import Dataset, DataLoader
import cv2
import numpy as np
import sys
import os

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from app.models.utils import preprocess_image_for_model
from app.config import settings, IMAGENET_MEAN, IMAGENET_STD


class ImagePairDataset(Dataset):
	def __init__(
		self,
		real_dir: Path,
		fake_dir: Path,
		size: Tuple[int, int] | None = None,
		use_face_detection: bool = False,
		min_face_size: int = 64,
		face_confidence: float = 0.85,
		face_padding: float = 0.2,
		use_lighting_normalization: bool = True,
		use_augment: bool = False,
	):
		self.real = sorted([p for p in Path(real_dir).glob("**/*") if p.suffix.lower() in {".jpg", ".png", ".jpeg"}])
		self.fake = sorted([p for p in Path(fake_dir).glob("**/*") if p.suffix.lower() in {".jpg", ".png", ".jpeg"}])
		self.samples: List[Tuple[Path, int]] = [(p, 0) for p in self.real] + [(p, 1) for p in self.fake]
		random.shuffle(self.samples)
		s = settings.MODEL_INPUT_SIZE
		self.size = size if size is not None else (s, s)
		self.use_face_detection = use_face_detection
		self.min_face_size = min_face_size
		self.face_confidence = face_confidence
		self.face_padding = face_padding
		self.use_lighting_normalization = use_lighting_normalization
		self.use_augment = use_augment

	def __len__(self) -> int:
		return len(self.samples)

	def __getitem__(self, idx: int):
		path, label = self.samples[idx]
		img = cv2.imread(str(path), cv2.IMREAD_COLOR)
		if img is None:
			raise ValueError(f"Could not read {path}")
		
		# Use the same preprocessing as inference (with optional face detection)
		if self.use_face_detection:
			tensor = preprocess_image_for_model(
				img,
				size=self.size,
				use_face_detection=True,
				min_face_size=self.min_face_size,
				face_confidence=self.face_confidence,
				face_padding=self.face_padding,
				use_lighting_normalization=self.use_lighting_normalization,
				use_imagenet_normalization=False,  # apply after augmentation
			)
		else:
			# Fallback to simple preprocessing
			if self.use_lighting_normalization:
				from app.models.utils import normalize_lighting
				img = normalize_lighting(img)
			img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
			img_resized = cv2.resize(img_rgb, self.size, interpolation=cv2.INTER_AREA)
			img_normalized = img_resized.astype(np.float32) / 255.0
			img_transposed = np.transpose(img_normalized, (2, 0, 1))
			tensor = torch.from_numpy(img_transposed).float()

		# Data augmentation (training only) - must run before ImageNet norm
		if self.use_augment:
			if random.random() < 0.5:
				tensor = torch.flip(tensor, dims=[2])  # horizontal flip
			# brightness
			bright = 0.6 + 0.8 * random.random()  # 0.6-1.4
			tensor = (tensor * bright).clamp(0.0, 1.0)
			# gamma
			gamma = 0.6 + 0.8 * random.random()  # 0.6-1.4
			tensor = torch.pow(tensor + 1e-6, gamma)
			# color shift
			tensor = tensor.clone()
			if random.random() < 0.5:
				tensor[0] = (tensor[0] * (0.9 + 0.2 * random.random())).clamp(0.0, 1.0)
			if random.random() < 0.5:
				tensor[2] = (tensor[2] * (0.9 + 0.2 * random.random())).clamp(0.0, 1.0)

		# ImageNet normalization for ResNet
		mean = torch.tensor(IMAGENET_MEAN).view(3, 1, 1)
		std = torch.tensor(IMAGENET_STD).view(3, 1, 1)
		tensor = (tensor - mean) / std
		
		y = torch.tensor([float(label)], dtype=torch.float32)
		return tensor, y


def make_loader(
	real_dir: str,
	fake_dir: str,
	batch_size: int = 16,
	shuffle: bool = True,
	num_workers: int = 0,
	use_face_detection: bool = False,
	min_face_size: int = 64,
	face_confidence: float = 0.85,
	face_padding: float = 0.2,
	use_lighting_normalization: bool = True,
	use_augment: bool = False,
) -> DataLoader:
	"""Create a DataLoader with optional face detection, lighting normalization, and augmentation."""
	ds = ImagePairDataset(
		Path(real_dir), 
		Path(fake_dir),
		use_face_detection=use_face_detection,
		min_face_size=min_face_size,
		face_confidence=face_confidence,
		face_padding=face_padding,
		use_lighting_normalization=use_lighting_normalization,
		use_augment=use_augment,
	)
	return DataLoader(ds, batch_size=batch_size, shuffle=shuffle, num_workers=num_workers)
















