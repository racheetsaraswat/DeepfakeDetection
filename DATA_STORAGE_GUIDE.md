# Data Storage Guide

This guide explains where to save different types of data in the DeepFake detection project.

## Default Data Directory Structure

By default, all data is stored in the `./data/` directory (relative to the backend folder):

```
data/
├── uploads/          # User-uploaded images/videos
├── frames/           # Extracted video frames (organized by job_id)
│   └── {job_id}/
│       ├── frame_0000.png
│       ├── frame_0001.png
│       └── ...
├── results/          # Inference results (heatmaps, etc.)
├── train/            # Training dataset
│   ├── real/         # Real images for training
│   └── fake/         # Fake images for training
├── val/              # Validation dataset (optional)
│   ├── real/
│   └── fake/
└── detector.pt       # Trained model checkpoint
```

## Data Types and Locations

### 1. **Training Data** (for model training)

**Location:** `data/train/real/` and `data/train/fake/`

```bash
# Create directories
mkdir -p data/train/real data/train/fake

# Add your images
# Real images go here:
data/train/real/
  ├── real_image_1.jpg
  ├── real_image_2.png
  └── ...

# Fake/deepfake images go here:
data/train/fake/
  ├── fake_image_1.jpg
  ├── fake_image_2.png
  └── ...
```

**Supported formats:** `.jpg`, `.jpeg`, `.png`

### 2. **Validation Data** (optional, for evaluation)

**Location:** `data/val/real/` and `data/val/fake/`

```bash
mkdir -p data/val/real data/val/fake
```

### 3. **Trained Model Checkpoint**

**Location:** `data/detector.pt`

The training script saves the model here by default. The API automatically loads it if it exists.

```bash
# After training, model is saved to:
data/detector.pt
```

### 4. **User Uploads** (automatic)

**Location:** `data/uploads/`

- Automatically created when users upload files via the API
- Files are saved with UUID prefixes to avoid conflicts
- Format: `{uuid}_{original_filename}`

**You don't need to manually save files here** - the API handles this.

### 5. **Video Frames** (automatic)

**Location:** `data/frames/{job_id}/`

- Automatically created when processing videos
- Each job gets its own subdirectory
- Frames are extracted and saved as PNG files

**You don't need to manually manage this** - the processing pipeline handles it.

### 6. **Inference Results** (automatic)

**Location:** `data/results/`

- Heatmaps and other result files are saved here
- Automatically managed by the inference pipeline

## Customizing Data Locations

You can change where data is stored using environment variables or a `.env` file:

### Create `.env` file in `backend/` directory:

```env
# Base data directory
DATA_DIR=./data

# Or use absolute paths:
# DATA_DIR=D:/DeepFake/data
# DATA_DIR=/path/to/your/data

# Individual directories (optional, defaults to DATA_DIR subdirectories)
UPLOADS_DIR=./data/uploads
FRAMES_DIR=./data/frames
RESULTS_DIR=./data/results
```

### Or set environment variables:

**Windows PowerShell:**
```powershell
$env:DATA_DIR="D:\DeepFake\data"
```

**Windows CMD:**
```cmd
set DATA_DIR=D:\DeepFake\data
```

**Linux/Mac:**
```bash
export DATA_DIR=/path/to/data
```

## Quick Setup Commands

### Create all necessary directories:

```bash
cd backend

# Create training directories
python train/quick_start.py

# Or manually:
mkdir -p data/train/real data/train/fake
mkdir -p data/val/real data/val/fake
mkdir -p data/uploads data/frames data/results
```

## Data Size Considerations

### Training Data
- **Minimum recommended:** 1,000+ images per class (real/fake)
- **Better:** 10,000+ images per class
- **Best:** 100,000+ images per class

### Storage Requirements
- **Images:** ~50-200 KB each (128x128 resized)
- **Videos:** Varies (original size preserved)
- **Frames:** ~50-200 KB each (extracted from videos)
- **Model checkpoint:** ~1-10 MB (depends on model size)

**Example:** 10,000 training images ≈ 1-2 GB

## Best Practices

1. **Keep training data separate from runtime data:**
   - Training: `data/train/` and `data/val/`
   - Runtime: `data/uploads/`, `data/frames/`, `data/results/`

2. **Use absolute paths for production:**
   ```env
   DATA_DIR=/var/deepfake/data
   ```

3. **Backup important data:**
   - Training datasets
   - Trained model checkpoints (`detector.pt`)

4. **Clean up old uploads/frames periodically:**
   - User uploads can accumulate
   - Video frames take up space
   - Consider implementing cleanup scripts

5. **Use external storage for large datasets:**
   - Point `DATA_DIR` to external drive/network storage
   - Useful for large training datasets

## Directory Permissions

Make sure the application has write permissions to the data directory:

**Windows:**
- Usually works by default in user directories
- May need admin rights for system directories

**Linux/Mac:**
```bash
chmod -R 755 data/
# Or for write access:
chmod -R 775 data/
```

## Example: Complete Setup

```bash
# 1. Navigate to backend
cd backend

# 2. Create all directories
python train/quick_start.py

# 3. Add training data
# Copy your real images to: data/train/real/
# Copy your fake images to: data/train/fake/

# 4. Train model (saves to data/detector.pt)
python train/train.py --epochs 10

# 5. The API will automatically use:
# - data/uploads/ for uploads
# - data/frames/ for video frames
# - data/results/ for results
# - data/detector.pt for the model
```

## Troubleshooting

### "Permission denied" errors
- Check directory permissions
- Ensure the app has write access
- Try running with appropriate user permissions

### "Directory not found" errors
- Directories are auto-created, but check if parent directory exists
- Verify `DATA_DIR` path is correct
- Check for typos in environment variables

### Running out of disk space
- Clean up old uploads: `data/uploads/`
- Clean up old frames: `data/frames/`
- Move training data to external storage
- Use symbolic links for large datasets













