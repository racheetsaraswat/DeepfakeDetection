from pathlib import Path
import cv2


def extract_frames(video_path: Path, dest_dir: Path, max_frames: int = 64):
    dest_dir.mkdir(parents=True, exist_ok=True)
    cap = cv2.VideoCapture(str(video_path))
    count = 0
    success, frame = cap.read()
    while success and count < max_frames:
        filename = dest_dir / f"{video_path.stem}_frame_{count:04d}.png"
        cv2.imwrite(str(filename), frame)
        count += 1
        success, frame = cap.read()
    cap.release()


def process_folder(source_dir: Path, target_dir: Path, max_frames: int = 64):
    if not source_dir.exists():
        return
    for video in source_dir.glob("*.*"):
        print(f"Extracting {video.name} -> {target_dir}")
        extract_frames(video, target_dir, max_frames=max_frames)


if __name__ == "__main__":
    base = Path("data")

    # Training videos
    video_train_real = base / "videos" / "train" / "real"
    video_train_fake = base / "videos" / "train" / "fake"
    train_real = base / "train" / "real"
    train_fake = base / "train" / "fake"

    process_folder(video_train_real, train_real)
    process_folder(video_train_fake, train_fake)

    # Validation videos (optional)
    video_val_real = base / "videos" / "val" / "real"
    video_val_fake = base / "videos" / "val" / "fake"
    val_real = base / "val" / "real"
    val_fake = base / "val" / "fake"

    process_folder(video_val_real, val_real)
    process_folder(video_val_fake, val_fake)
