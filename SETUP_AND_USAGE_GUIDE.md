# Complete Setup and Usage Guide

## 📋 Is the Code Complete?

**Yes, the code is complete and functional**, but it's designed as a **scaffold/demo**:

✅ **What's Working:**
- Full-stack application (Frontend + Backend + Database)
- File upload system (images & videos)
- Deepfake detection inference pipeline
- Training scripts and data loaders
- MongoDB integration
- Background job processing

⚠️ **What's a Scaffold:**
- The model (`SimpleConvDiscriminator`) is a simple 3-layer CNN - **you need to train it** or replace it with a more sophisticated model
- The model needs training data to be useful
- Current model is for educational/demo purposes

---

## 🚀 Quick Start Guide

### Prerequisites

1. **Python 3.10+** installed
2. **Node.js 18+** installed
3. **MongoDB** running locally (default: `mongodb://localhost:27017`)
4. **GPU** (optional but recommended for training)

---

## 📦 Step 1: Backend Setup

### 1.1 Install Backend Dependencies

```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows PowerShell:
.\.venv\Scripts\Activate.ps1
# Windows CMD:
.\.venv\Scripts\activate.bat
# Linux/Mac:
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 1.2 Start MongoDB

**Windows:**
```bash
# If MongoDB is installed as a service, it should start automatically
# Or start manually:
mongod
```

**Linux/Mac:**
```bash
# Start MongoDB service
sudo systemctl start mongod
# Or:
mongod
```

**Verify MongoDB is running:**
- Open browser: `http://localhost:27017` (should show MongoDB connection message)
- Or check: `mongosh` (MongoDB shell)

---

## 🎨 Step 2: Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Frontend will be available at: **http://localhost:5173**

---

## 🧠 Step 3: Training the Model

### 3.1 Prepare Training Data

**Option A: Use Quick Start Script**
```bash
cd backend
python train/quick_start.py
```

This creates the directory structure:
```
data/
├── train/
│   ├── real/      # Put real images here
│   └── fake/      # Put fake/deepfake images here
└── val/           # Optional validation set
    ├── real/
    └── fake/
```

**Option B: Manual Setup**
```bash
# Create directories manually
mkdir -p data/train/real
mkdir -p data/train/fake
mkdir -p data/val/real
mkdir -p data/val/fake
```

### 3.2 Add Your Dataset

**Where to get datasets:**
- **FaceForensics++**: https://github.com/ondyari/FaceForensics
- **DFDC (Deepfake Detection Challenge)**: https://www.kaggle.com/c/deepfake-detection-challenge
- **Celeb-DF**: https://github.com/yuezunli/celeb-deepfakeforensics

**Copy images:**
```bash
# Copy real images
cp /path/to/real/images/* data/train/real/

# Copy fake images
cp /path/to/fake/images/* data/train/fake/
```

**Requirements:**
- Supported formats: `.jpg`, `.jpeg`, `.png`
- Images will be auto-resized to 128x128 during training
- Balanced dataset recommended (similar number of real/fake images)

### 3.3 Start Training

**Basic Training (Default Settings):**
```bash
cd backend
python train/train.py
```

**Custom Training:**
```bash
python train/train.py \
  --real-dir ./data/train/real \
  --fake-dir ./data/train/fake \
  --epochs 20 \
  --lr 0.001 \
  --batch-size 32 \
  --save-path ./data/detector.pt
```

**Training Parameters:**
- `--epochs`: Number of training epochs (default: 10)
- `--lr`: Learning rate (default: 0.001)
- `--batch-size`: Batch size (default: 16, increase if you have GPU memory)
- `--real-dir`: Directory with real images
- `--fake-dir`: Directory with fake images
- `--save-path`: Where to save the trained model (default: `./data/detector.pt`)

### 3.4 Training Time Estimates

**Training time depends on:**
- Dataset size (number of images)
- Number of epochs
- Hardware (CPU vs GPU)
- Batch size

**Example Estimates:**

| Dataset Size | Epochs | Hardware | Estimated Time |
|-------------|--------|----------|----------------|
| 1,000 images | 10 | CPU | 2-4 hours |
| 1,000 images | 10 | GPU (GTX 1060) | 15-30 minutes |
| 10,000 images | 10 | CPU | 1-2 days |
| 10,000 images | 10 | GPU (RTX 3080) | 1-3 hours |
| 100,000 images | 20 | GPU (RTX 4090) | 4-8 hours |

**For a typical project:**
- **Small dataset (1K-5K images)**: 1-6 hours on GPU, 1-2 days on CPU
- **Medium dataset (10K-50K images)**: 2-12 hours on GPU, 3-7 days on CPU
- **Large dataset (100K+ images)**: 1-3 days on GPU, weeks on CPU

**Tips to speed up training:**
- Use GPU if available
- Increase batch size (if GPU memory allows)
- Use fewer epochs for initial testing
- Use data augmentation to artificially increase dataset size

### 3.5 Monitor Training

Training will print progress after each epoch:
```
Epoch 1/10 - Loss: 0.6234 (batches: 125)
[Checkpoint] Saved model to ./data/detector.pt after epoch 1
```

**Check GPU usage (if using NVIDIA GPU):**
```bash
nvidia-smi
```

### 3.6 Evaluate Trained Model

After training, evaluate on validation set:
```bash
python train/eval.py
```

Or with custom paths:
```bash
python train/eval.py \
  --real-dir ./data/val/real \
  --fake-dir ./data/val/fake \
  --ckpt-path ./data/detector.pt
```

---

## 🔍 Step 4: Running Detection (Inference)

### 4.1 Start Backend Server

**Terminal 1 - Backend:**
```bash
cd backend

# Activate virtual environment (if not already active)
.\.venv\Scripts\Activate.ps1  # Windows PowerShell
# or
source .venv/bin/activate     # Linux/Mac

# Start FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Backend will be available at: **http://localhost:8000**

**Verify backend is running:**
- Open browser: `http://localhost:8000`
- Should see: `{"status": "ok"}`

### 4.2 Start Frontend

**Terminal 2 - Frontend:**
```bash
cd frontend
npm run dev
```

Frontend will be available at: **http://localhost:5173**

### 4.3 Use the Application

1. **Open browser**: http://localhost:5173
2. **Read the landing page** about deepfakes
3. **Click "Start Deepfake Detection"**
4. **Upload an image or video** on the home page
5. **View results** - the system will:
   - Upload your file
   - Process it through the model
   - Show detection score (0.0 = Real, 1.0 = Fake)
   - Display label (REAL or FAKE)

---

## 📝 Complete Command Reference

### Training Commands

```bash
# Setup training directories
cd backend
python train/quick_start.py

# Basic training (10 epochs, default settings)
python train/train.py

# Custom training
python train/train.py --epochs 20 --batch-size 32 --lr 0.0005

# Evaluate model
python train/eval.py
```

### Detection/Inference Commands

```bash
# Terminal 1: Start Backend
cd backend
.\.venv\Scripts\Activate.ps1  # Windows
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Terminal 2: Start Frontend
cd frontend
npm run dev
```

### Database Commands

```bash
# Check MongoDB is running
mongosh

# Or check connection
# Open browser: http://localhost:27017
```

---

## 🐛 Troubleshooting

### Backend Issues

**"MongoDB connection error":**
- Make sure MongoDB is running: `mongod` or check service status
- Verify connection: `mongosh`

**"500 Internal Server Error":**
- Check backend logs for error details
- Verify MongoDB is accessible
- Check if model file exists: `./data/detector.pt`

**"Module not found":**
- Activate virtual environment: `.\.venv\Scripts\Activate.ps1`
- Reinstall dependencies: `pip install -r requirements.txt`

### Frontend Issues

**"Failed to fetch" or CORS errors:**
- Make sure backend is running on port 8000
- Check `VITE_API_BASE` in `.env` file (if using custom URL)
- Verify backend CORS settings in `backend/app/main.py`

**"Cannot connect to backend":**
- Start backend server first: `uvicorn app.main:app --reload`
- Check backend URL: http://localhost:8000

### Training Issues

**"Out of Memory (OOM)":**
- Reduce batch size: `--batch-size 8` or `--batch-size 4`
- Use smaller images
- Close other applications using GPU

**"No training samples found":**
- Check directory paths: `--real-dir` and `--fake-dir`
- Verify images are in correct folders
- Check file formats (jpg, png, jpeg)

**"Slow training":**
- Use GPU if available
- Increase batch size (if memory allows)
- Use fewer workers or disable multiprocessing

---

## 📊 Project Structure

```
DeepFake/
├── backend/
│   ├── app/
│   │   ├── api/          # FastAPI endpoints
│   │   ├── models/       # PyTorch model definitions
│   │   ├── inference/    # Inference pipeline
│   │   └── main.py       # FastAPI app
│   ├── train/            # Training scripts
│   │   ├── train.py      # Main training script
│   │   ├── eval.py       # Evaluation script
│   │   └── data_loader.py
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── pages/        # React pages
│   │   ├── components/   # React components
│   │   └── services/     # API client
│   └── package.json
└── data/                 # Training data & models
    ├── train/
    ├── detector.pt      # Trained model (after training)
    └── uploads/         # Uploaded files
```

---

## ✅ Checklist: Is Everything Ready?

- [ ] Python 3.10+ installed
- [ ] Node.js 18+ installed
- [ ] MongoDB installed and running
- [ ] Backend dependencies installed (`pip install -r requirements.txt`)
- [ ] Frontend dependencies installed (`npm install`)
- [ ] Training data prepared (real and fake images)
- [ ] Model trained (`python train/train.py`)
- [ ] Backend server running (`uvicorn app.main:app --reload`)
- [ ] Frontend server running (`npm run dev`)
- [ ] Can access frontend at http://localhost:5173
- [ ] Can access backend at http://localhost:8000

---

## 🎯 Next Steps

1. **Train your model** with your dataset
2. **Evaluate** the model performance
3. **Test** via the web interface
4. **Improve** the model architecture if needed
5. **Deploy** to production (when ready)

---

## 📚 Additional Resources

- **Training Guide**: `backend/TRAINING_GUIDE.md`
- **Backend README**: `backend/README_BACKEND.md`
- **Frontend README**: `frontend/README_FRONTEND.md`
- **Data Storage Guide**: `DATA_STORAGE_GUIDE.md`

---

## ⚠️ Important Notes

1. **This is a demo/scaffold** - the model needs training to be useful
2. **Not for production** - this is for educational purposes
3. **Model accuracy** depends on training data quality and quantity
4. **GPU recommended** for training - CPU training is very slow
5. **MongoDB required** - the app won't work without it

---

**Good luck with your deepfake detection project! 🚀**
