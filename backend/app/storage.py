from pathlib import Path
from typing import Tuple
import uuid
import shutil

from .config import settings


def ensure_dirs() -> None:
	settings.DATA_DIR.mkdir(parents=True, exist_ok=True)
	settings.UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
	settings.FRAMES_DIR.mkdir(parents=True, exist_ok=True)
	settings.RESULTS_DIR.mkdir(parents=True, exist_ok=True)


def save_upload(tmp_path: Path, filename: str) -> Path:
	ensure_dirs()
	safe_name = f"{uuid.uuid4().hex}_{filename}"
	dest = settings.UPLOADS_DIR / safe_name
	shutil.move(str(tmp_path), dest)
	return dest


def make_job_frame_dir(job_id: str) -> Path:
	dir_path = settings.FRAMES_DIR / job_id
	dir_path.mkdir(parents=True, exist_ok=True)
	return dir_path


def path_for_result(name: str) -> Path:
	ensure_dirs()
	return settings.RESULTS_DIR / name
















