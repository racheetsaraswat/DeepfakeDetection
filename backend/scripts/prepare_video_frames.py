from pathlib import Path
from typing import Iterable

import sys
import os

# Ensure we can import the backend app package when run as a script
backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

import cv2


VIDEO_EXTS = {".mp4", ".avi", ".mov", ".mkv", ".webm"}


def extract_video_frames(video_path: Path, out_dir: Path, max_frames: int = 32) -> int:
    """
    Lightweight frame extractor that does NOT import torch/tensorflow.

    Saves frames as PNGs:
      out_dir/frame_0000.png, ...

    Returns number of frames written.
    """
    out_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    if not cap.isOpened():
        print(f"    ! Could not open video: {video_path}")
        return 0

    total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT) or 0)
    # Uniformly sample up to max_frames across the whole video
    step = max(1, total // max_frames) if total > 0 else 1

    written = 0
    idx = 0
    while written < max_frames:
        ok, frame = cap.read()
        if not ok:
            break
        if idx % step == 0:
            filename = out_dir / f"frame_{written:04d}.png"
            cv2.imwrite(str(filename), frame)
            written += 1
        idx += 1

    cap.release()
    return written


def iter_videos(root: Path) -> Iterable[Path]:
    if not root.exists():
        return []
    return [p for p in root.rglob("*") if p.suffix.lower() in VIDEO_EXTS]


def prepare_split(split: str, max_frames: int = 32) -> None:
    """
    Extract frames from videos into the existing image-based train/val folders.

    Expected layout:
      data/videos/{split}/real/*.mp4
      data/videos/{split}/fake/*.mp4

    Frames will be written under:
      data/{split}/real/<video_stem>/frame_0000.png
      data/{split}/fake/<video_stem>/frame_0000.png
    """
    base = backend_dir / "data"

    src_real = base / "videos" / split / "real"
    src_fake = base / "videos" / split / "fake"

    dst_real_root = base / split / "real"
    dst_fake_root = base / split / "fake"

    print(f"\n=== Preparing {split} split ===")
    print(f"Source real videos: {src_real}")
    print(f"Source fake videos: {src_fake}")

    real_videos = iter_videos(src_real)
    fake_videos = iter_videos(src_fake)

    print(f"Found {len(real_videos)} real videos, {len(fake_videos)} fake videos.")

    for v in real_videos:
        out_dir = dst_real_root / v.stem
        print(f"  [real] {v.name} -> {out_dir} (max_frames={max_frames})")
        extract_video_frames(v, out_dir, max_frames=max_frames)

    for v in fake_videos:
        out_dir = dst_fake_root / v.stem
        print(f"  [fake] {v.name} -> {out_dir} (max_frames={max_frames})")
        extract_video_frames(v, out_dir, max_frames=max_frames)


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Extract frames from training/validation videos into image folders.")
    parser.add_argument(
        "--max-frames",
        type=int,
        default=32,
        help="Max frames to extract per video (default: 32).",
    )
    parser.add_argument(
        "--splits",
        type=str,
        default="train,val",
        help="Comma-separated list of splits to prepare (default: train,val).",
    )

    args = parser.parse_args()
    splits = [s.strip() for s in args.splits.split(",") if s.strip()]

    print(f"Backend dir: {backend_dir}")
    print(f"Preparing splits: {splits}")

    for split in splits:
        prepare_split(split, max_frames=args.max_frames)

    print("\nDone. You can now train with the usual image-based training script:")
    print("  python train/train.py --epochs 5 --batch-size 8")


if __name__ == "__main__":
    main()

