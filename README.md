Deepfake Detection Website (Images & Videos)
===========================================

End-to-end scaffold for a GAN-based deepfake detection website that supports images and videos, designed to run locally without Docker. Includes a FastAPI backend with Celery background workers, MongoDB (Motor) persistence, PyTorch model scaffold, and a React + Tailwind frontend.

Stack
-----
- Backend/ML: Python 3.10+, FastAPI, PyTorch, MongoDB (Motor)
- Background Tasks: FastAPI BackgroundTasks (default, no Redis needed) or Celery + Redis (optional)
- Frontend: React (Vite) + TypeScript + Tailwind CSS
- Database: MongoDB (local)
- Testing: pytest (backend), vitest + @testing-library/react (frontend)
- Environment: venv + requirements.txt

Getting Started (Local, no Docker)
----------------------------------
1) Prerequisites
- Python 3.10+
- Node.js 18+
- MongoDB running locally (default: mongodb://localhost:27017)
- Redis (optional): Only needed if using Celery workers. See `backend/REDIS_ALTERNATIVES.md` for details.

2) Environment
- Copy `.env.example` to `.env` and adjust values as needed.

3) Backend
- Create venv and install:
  - `cd backend`
  - `python -m venv .venv`
  - Windows PowerShell: `.\.venv\Scripts\Activate.ps1`
  - `pip install -r requirements.txt`
- Run API (no Redis needed by default): 
  - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
- Optional: Start Celery worker (only if using Redis):
  - `celery -A app.workers.tasks.celery_app worker --loglevel=INFO`
  
  **Note:** By default, the app uses FastAPI BackgroundTasks which doesn't require Redis or a separate worker process. See `backend/REDIS_ALTERNATIVES.md` for more options.

4) Frontend
- `cd frontend`
- `npm install`
- `npm run dev` (default on http://localhost:5173)

5) Directory Layout
- See the tree in your request; files have been created to match it.

Key Endpoints
-------------
- POST `/upload` (multipart/form-data): Upload image/video. Returns `{ job_id }`, queues background job if video.
- GET `/jobs/{id}`: Returns job metadata and status.
- GET `/results/{id}`: Returns aggregated inference results for a job.
- POST `/inference/predict` (image only): Synchronous image prediction.

Notes
-----
- The GAN/CNN model is a simple scaffold. Replace with your real model later.
- **Training**: See `backend/TRAINING_GUIDE.md` for detailed training instructions
- **Data Storage**: See `DATA_STORAGE_GUIDE.md` for where to save training data, models, and runtime files
- Local file storage (default locations):
  - Training data: `data/train/real/` and `data/train/fake/`
  - Model checkpoint: `data/detector.pt` (created after training)
  - Uploads: `data/uploads` (automatic)
  - Frames: `data/frames/{job_id}` (automatic)
  - Results: `data/results` (automatic)

Security and Privacy
--------------------
- See `PRIVACY.md` and `DISCLAIMER.md`. Do not upload sensitive data to demo setups.

License
-------
- MIT — see `LICENSE`.



