"""
Quick start script for training - creates sample directory structure and provides examples.
Run this to set up training directories and see example commands.
"""
from pathlib import Path

def setup_training_dirs():
	"""Create training directory structure"""
	dirs = [
		"data/train/real",
		"data/train/fake",
		"data/val/real",
		"data/val/fake",
	]
	
	for dir_path in dirs:
		Path(dir_path).mkdir(parents=True, exist_ok=True)
		print(f"Created: {dir_path}")
	
	print("\n[OK] Directory structure created!")
	print("\nNext steps:")
	print("1. Add your real images to: data/train/real/")
	print("2. Add your fake images to: data/train/fake/")
	print("3. (Optional) Add validation images to: data/val/real/ and data/val/fake/")
	print("\n4. Run training:")
	print("   python train/train.py --epochs 10 --batch-size 16")
	print("\n5. Evaluate:")
	print("   python train/eval.py")


if __name__ == "__main__":
	setup_training_dirs()

