# Face Detection and Preprocessing Guide

## Overview

The deepfake detection system now includes automatic face detection and extraction as part of the preprocessing pipeline. This significantly improves detection accuracy by focusing the model on facial regions where deepfake artifacts are most visible.

## How It Works

1. **Face Detection**: Uses MTCNN (Multi-task CNN) to detect faces in images/video frames
2. **Face Extraction**: Extracts the largest detected face with configurable padding
3. **Fallback**: If no face is detected, the system falls back to processing the full image
4. **Preprocessing**: The extracted face is resized to 128x128 and normalized for model input

## Configuration

Face detection can be configured via environment variables or `.env` file:

```bash
# Enable/disable face detection (default: true)
USE_FACE_DETECTION=true

# Minimum face size in pixels (default: 64)
MIN_FACE_SIZE=64

# Face detection confidence (default: 0.85, retries at 0.75/0.6 for challenging lighting)
FACE_DETECTION_CONFIDENCE=0.85

# Lighting normalization via CLAHE (default: true) - helps dramatic/indoor/warm lighting
USE_LIGHTING_NORMALIZATION=true

# Padding ratio around detected face (default: 0.2 = 20%)
FACE_PADDING=0.2

# Detection thresholds: REAL < UNCERTAIN_LOW, UNCERTAIN in [low, high), FAKE >= UNCERTAIN_HIGH
UNCERTAIN_LOW=0.4
UNCERTAIN_HIGH=0.9
```

## Installation

Install the required dependencies:

```bash
pip install mtcnn facenet-pytorch
```

Or install all requirements:

```bash
pip install -r requirements.txt
```

## Usage

### Automatic (Default)

Face detection is enabled by default. The inference pipeline automatically detects and extracts faces:

```python
from app.models.utils import load_image_bgr, preprocess_image_for_model

img = load_image_bgr("path/to/image.jpg")
tensor = preprocess_image_for_model(img)  # Automatically uses face detection
```

### Manual Control

You can control face detection behavior:

```python
# With face detection (default)
tensor = preprocess_image_for_model(
    img,
    use_face_detection=True,
    min_face_size=64,
    face_confidence=0.9,
    face_padding=0.2
)

# Without face detection (fallback to full image)
tensor = preprocess_image_for_model(
    img,
    use_face_detection=False
)
```

### Testing Face Detection

Test face detection on an image:

```bash
cd backend
python scripts/test_face_detection.py path/to/image.jpg --output face_crop.jpg
```

This will:
- Detect faces in the image
- Extract the largest face
- Save the cropped face (if `--output` provided)
- Create a visualization with bounding boxes

### Testing with Inference

Test the full pipeline with face detection:

```bash
cd backend
python scripts/test_image.py path/to/image.jpg
```

To disable face detection for testing:

```bash
python scripts/test_image.py path/to/image.jpg --no-face-detection
```

## Training with Face Detection

When training, you can optionally use face detection preprocessing:

```python
from train.data_loader import make_loader

# With face detection
loader = make_loader(
    real_dir="./data/train/real",
    fake_dir="./data/train/fake",
    use_face_detection=True,
    min_face_size=64,
    face_confidence=0.9,
    face_padding=0.2
)

# Without face detection (original behavior)
loader = make_loader(
    real_dir="./data/train/real",
    fake_dir="./data/train/fake",
    use_face_detection=False
)
```

**Note**: If your training dataset already contains cropped faces, you may want to disable face detection during training to avoid double-processing.

## Troubleshooting

### No Faces Detected

If face detection fails:

1. **Lower confidence threshold**: Try `FACE_DETECTION_CONFIDENCE=0.7` or lower
2. **Lower minimum face size**: Try `MIN_FACE_SIZE=40` for smaller faces
3. **Check image quality**: Ensure faces are clearly visible and front-facing
4. **Check image format**: Ensure images are in supported formats (JPEG, PNG)

### Performance Issues

Face detection adds processing time:

- **CPU**: ~100-500ms per image
- **GPU**: ~20-100ms per image (if CUDA available)

For faster processing:
- Use GPU if available (automatic)
- Reduce `MIN_FACE_SIZE` to skip very small faces
- Increase `FACE_DETECTION_CONFIDENCE` to reduce false positives

### Memory Issues

MTCNN can use significant memory. If you encounter OOM errors:

- Process images in smaller batches
- Reduce image resolution before face detection
- Use CPU mode if GPU memory is limited

## Technical Details

### MTCNN Face Detector

- **Algorithm**: Multi-task Cascaded Convolutional Networks
- **Features**: 
  - Face detection with bounding boxes
  - Facial landmark detection (optional)
  - Confidence scores
- **Device**: Automatically uses GPU if available, falls back to CPU

### Face Extraction Process

1. Detect all faces in image
2. Filter by confidence and minimum size
3. Select largest face (by area)
4. Add padding around face bounding box
5. Crop and return face region
6. If no face found, return full image

### Integration Points

Face detection is integrated at:

- **Inference**: `app/inference/run_inference.py`
- **Preprocessing**: `app/models/utils.py`
- **Training**: `train/data_loader.py` (optional)
- **API**: Automatic in upload/inference endpoints

## Best Practices

1. **Training**: 
   - Use face detection if training on full images
   - Disable if training on pre-cropped faces
   - Ensure consistent preprocessing between training and inference

2. **Inference**:
   - Keep face detection enabled for best accuracy
   - Adjust thresholds based on your use case
   - Monitor detection rates in logs

3. **Video Processing**:
   - Face detection runs on each frame
   - Consider frame sampling to reduce processing time
   - Monitor for frames with no faces detected

## Future Improvements

Potential enhancements:

- Support for multiple faces (select best or process all)
- Face alignment/normalization
- Alternative face detectors (RetinaFace, YOLOv5-face)
- Batch face detection for faster processing
- Face quality scoring to filter poor detections
