import os
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
import asyncio
from ..db.mongodb import connect_to_mongo
from ..db import models as db_models
from ..inference.run_inference import extract_video_frames, run_video_inference, run_image_inference
from ..storage import make_job_frame_dir

# Thread pool for CPU-intensive tasks (video/image processing)
_executor = ThreadPoolExecutor(max_workers=2, thread_name_prefix="inference")

# Optional: Keep Celery support if REDIS_URL is set
try:
	from celery import Celery
	from ..config import settings
	# Use Celery only if explicitly configured (not default localhost)
	USE_CELERY = hasattr(settings, 'REDIS_URL') and settings.REDIS_URL and settings.REDIS_URL != "redis://localhost:6379/0"
except:
	USE_CELERY = False

if USE_CELERY:
	celery_app = Celery(
		"deepfake_tasks",
		broker=settings.REDIS_URL,
		backend=settings.CELERY_RESULT_BACKEND,
	)

	@celery_app.task(name="process_file")
	def process_file(job_id: str, file_path: str, file_type: str) -> None:
		import asyncio
		asyncio.run(process_file_async(job_id, file_path, file_type))


def _process_video_sync(job_id: str, file_path: Path, frame_dir: Path) -> tuple:
	"""Synchronous video processing - runs in thread pool"""
	frames = extract_video_frames(file_path, frame_dir, max_frames=64)
	avg_score, label, per_frame_scores = run_video_inference(frames)
	return {
		"status": "completed",
		"score": float(avg_score),
		"label": label,
		"frames": [str(p) for p in frames],
	}


def _process_image_sync(file_path: Path) -> dict:
	"""Synchronous image processing - runs in thread pool"""
	result = run_image_inference(file_path)
	return {
		"status": "completed",
		"score": float(result["score"]),
		"label": result["label"],
		"frames": [],
	}


async def process_file_async(job_id: str, file_path: str, file_type: str) -> None:
	"""Process file asynchronously - works with both BackgroundTasks and Celery.
	CPU-intensive work runs in thread pool to avoid blocking the event loop."""
	await connect_to_mongo()
	await db_models.update_job(job_id, {"status": "processing"})
	path = Path(file_path)
	
	try:
		loop = asyncio.get_event_loop()
		
		if file_type == "video":
			frame_dir = make_job_frame_dir(job_id)
			# Run CPU-intensive work in thread pool
			result = await loop.run_in_executor(
				_executor, 
				_process_video_sync, 
				job_id, 
				path, 
				frame_dir
			)
			await db_models.update_job(job_id, result)
		else:
			# Run CPU-intensive work in thread pool
			result = await loop.run_in_executor(
				_executor,
				_process_image_sync,
				path
			)
			await db_models.update_job(job_id, result)
	except Exception as e:
		await db_models.update_job(job_id, {"status": "failed", "error": str(e)})



