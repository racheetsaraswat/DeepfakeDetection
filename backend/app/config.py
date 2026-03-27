import os
from pathlib import Path
from dotenv import load_dotenv

# Load .env from backend root; override=True ensures .env wins over existing env vars
_backend_dir = Path(__file__).resolve().parent.parent
load_dotenv(_backend_dir / ".env", override=True)


class Settings:
	API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
	API_PORT: int = int(os.getenv("API_PORT", "8000"))

	MONGO_URL: str = os.getenv("MONGO_URL", "mongodb://localhost:27017")
	MONGO_DB: str = os.getenv("MONGO_DB", "deepfake_db")
	MONGO_JOBS_COLLECTION: str = os.getenv("MONGO_JOBS_COLLECTION", "jobs")

	REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379/0")
	CELERY_RESULT_BACKEND: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/1")

	DATA_DIR: Path = Path(os.getenv("DATA_DIR", "./data")).resolve()
	UPLOADS_DIR: Path = Path(os.getenv("UPLOADS_DIR", "./data/uploads")).resolve()
	FRAMES_DIR: Path = Path(os.getenv("FRAMES_DIR", "./data/frames")).resolve()
	RESULTS_DIR: Path = Path(os.getenv("RESULTS_DIR", "./data/results")).resolve()
	
	# Face detection settings
	USE_FACE_DETECTION: bool = os.getenv("USE_FACE_DETECTION", "true").lower().strip() in ("true", "1", "yes")
	MIN_FACE_SIZE: int = int(os.getenv("MIN_FACE_SIZE", "64"))
	FACE_DETECTION_CONFIDENCE: float = float(os.getenv("FACE_DETECTION_CONFIDENCE", "0.85"))  # Lower for dramatic/indoor lighting
	FACE_PADDING: float = float(os.getenv("FACE_PADDING", "0.2"))  # 20% padding around face
	USE_LIGHTING_NORMALIZATION: bool = os.getenv("USE_LIGHTING_NORMALIZATION", "true").lower() == "true"  # CLAHE for challenging lighting

	# Detection thresholds: REAL < uncertain_low, UNCERTAIN in [low, high), FAKE >= high
	UNCERTAIN_LOW: float = float(os.getenv("UNCERTAIN_LOW", "0.4"))
	UNCERTAIN_HIGH: float = float(os.getenv("UNCERTAIN_HIGH", "0.9"))  # 0.9 = only very confident fakes labeled FAKE

	# ResNet input (ImageNet standard)
	MODEL_INPUT_SIZE: int = 224


# ImageNet normalization for pretrained models
IMAGENET_MEAN = (0.485, 0.456, 0.406)
IMAGENET_STD = (0.229, 0.224, 0.225)


settings = Settings()
















