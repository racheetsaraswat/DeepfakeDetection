from pathlib import Path
import numpy as np
import cv2
from ..storage import path_for_result


def save_dummy_heatmap(image_path: Path, score: float) -> Path:
	# Create a simple red overlay proportional to score
	img = cv2.imread(str(image_path), cv2.IMREAD_COLOR)
	if img is None:
		return path_for_result("missing.png")
	h, w = img.shape[:2]
	overlay = np.zeros((h, w, 3), dtype=np.uint8)
	overlay[:, :, 2] = int(min(max(score, 0.0), 1.0) * 255)
	heatmap = cv2.addWeighted(img, 0.6, overlay, 0.4, 0)
	out_path = path_for_result(f"heatmap_{image_path.stem}.png")
	cv2.imwrite(str(out_path), heatmap)
	return out_path
















