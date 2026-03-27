"""
Test script to verify face detection functionality.
This script tests face detection on sample images without running inference.
"""
import argparse
import sys
from pathlib import Path

# Add parent directory to path so we can import app modules
sys.path.insert(0, str(Path(__file__).parent.parent))

import cv2
import numpy as np
from app.models.utils import (
	load_image_bgr, 
	detect_faces, 
	extract_face_region,
	detect_and_extract_largest_face
)
from app.config import settings


def main():
	parser = argparse.ArgumentParser(description="Test face detection on images")
	parser.add_argument("image", help="Path to image file")
	parser.add_argument("--output", help="Path to save detected face (optional)")
	parser.add_argument("--min-size", type=int, default=settings.MIN_FACE_SIZE,
					   help="Minimum face size in pixels")
	parser.add_argument("--confidence", type=float, default=settings.FACE_DETECTION_CONFIDENCE,
					   help="Face detection confidence threshold")
	args = parser.parse_args()

	image_path = Path(args.image)
	if not image_path.exists():
		raise FileNotFoundError(f"Image not found: {image_path}")

	# Load image
	img_bgr = load_image_bgr(str(image_path))
	img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
	
	print(f"Testing face detection on: {image_path}")
	print(f"Image size: {img_rgb.shape[1]}x{img_rgb.shape[0]}")
	print(f"Settings: min_size={args.min_size}, confidence={args.confidence}")
	print()
	
	# Detect faces
	faces = detect_faces(img_rgb, min_face_size=args.min_size, confidence=args.confidence)
	
	if not faces:
		print("[X] No faces detected")
		print("\nTips:")
		print("- Try lowering --confidence (e.g., 0.7)")
		print("- Try lowering --min-size (e.g., 40)")
		print("- Ensure the image contains clear, front-facing faces")
		return
	
	print(f"[OK] Detected {len(faces)} face(s):")
	for i, face in enumerate(faces):
		x, y, w, h = face['box']
		confidence = face['confidence']
		print(f"  Face {i+1}:")
		print(f"    Position: ({x}, {y})")
		print(f"    Size: {w}x{h}")
		print(f"    Confidence: {confidence:.3f}")
	
	# Extract largest face
	largest_face = detect_and_extract_largest_face(
		img_rgb,
		min_face_size=args.min_size,
		confidence=args.confidence,
		padding=settings.FACE_PADDING
	)
	
	if largest_face is not None:
		print(f"\n[OK] Extracted face region: {largest_face.shape[1]}x{largest_face.shape[0]}")
		
		# Save if output path provided
		if args.output:
			output_path = Path(args.output)
			output_path.parent.mkdir(parents=True, exist_ok=True)
			cv2.imwrite(str(output_path), cv2.cvtColor(largest_face, cv2.COLOR_RGB2BGR))
			print(f"[OK] Saved face crop to: {output_path}")
		
		# Visualize detection on original image
		vis_img = img_bgr.copy()
		x, y, w, h = max(faces, key=lambda f: f['box'][2] * f['box'][3])['box']
		cv2.rectangle(vis_img, (x, y), (x + w, y + h), (0, 255, 0), 2)
		cv2.putText(vis_img, f"Face: {max(f['confidence'] for f in faces):.2f}", 
				   (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
		
		vis_path = image_path.parent / f"{image_path.stem}_detected{image_path.suffix}"
		cv2.imwrite(str(vis_path), vis_img)
		print(f"[OK] Saved visualization to: {vis_path}")
	else:
		print("\n[X] Failed to extract face region")


if __name__ == "__main__":
	main()
