Backend (FastAPI + Celery + MongoDB)
====================================

Run
---
1) Create venv and install requirements:
   - `python -m venv .venv` (or `python -m venv venv`)
   - Windows PowerShell: `.\.venv\Scripts\Activate.ps1` (or `.\venv\Scripts\Activate.ps1`)
   - `pip install -r requirements.txt`

   **Note**: Face detection dependencies (mtcnn, facenet-pytorch) are included in requirements.txt.
   If you encounter import errors, run the setup script:
   - PowerShell: `.\setup_face_detection.ps1`
   - CMD: `setup_face_detection.bat`

2) Ensure MongoDB and Redis are running locally.

3) Start API:
   - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`

4) Start Celery worker:
   - `celery -A app.workers.tasks.celery_app worker --loglevel=INFO`

Environment
-----------
Set via `.env` or system environment variables. See `.env.example` at repo root for common values.

Key Paths
---------
- Uploads: `data/uploads`
- Frames: `data/frames/{job_id}`
- Results: `data/results`

Notes
-----
- The model in `app/models/detector.py` is a scaffold. Replace with your trained model later.
- Video pipeline extracts frames via OpenCV and aggregates per-frame scores.
- **Face Detection**: Enabled by default. Automatically detects and extracts faces before inference.
  See `FACE_DETECTION_GUIDE.md` for configuration and usage details.
















