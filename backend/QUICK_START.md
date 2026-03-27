# Quick Start Guide - Face Detection Setup

## PowerShell Execution Policy Issue?

If you see "running scripts is disabled on this system", use one of these methods:

### Method 1: Use Batch File (Easiest)

```cmd
cd "E:\New folder\Telegram Desktop\DeepFake\DeepFake\backend"
venv\Scripts\activate.bat
python scripts/test_face_detection.py image.jpg
```

### Method 2: Use Python Directly (No Activation Needed)

```powershell
cd "E:\New folder\Telegram Desktop\DeepFake\DeepFake\backend"
.\venv\Scripts\python.exe scripts/test_face_detection.py image.jpg
```

### Method 3: Temporarily Change Execution Policy

```powershell
# Check current policy
Get-ExecutionPolicy

# Set for current session only (safest)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Then activate normally
.\venv\Scripts\Activate.ps1
```

### Method 4: Bypass for Single Script

```powershell
powershell -ExecutionPolicy Bypass -File .\venv\Scripts\Activate.ps1
```

## Running Scripts

### Test Face Detection
```powershell
# Using direct Python path
.\venv\Scripts\python.exe scripts/test_face_detection.py "path/to/image.jpg" --output face_crop.jpg
```

### Test Full Inference
```powershell
.\venv\Scripts\python.exe scripts/test_image.py "path/to/image.jpg"
```

### Start API Server
```powershell
.\venv\Scripts\python.exe -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

## Alternative: Use CMD Instead

If PowerShell continues to cause issues, use Command Prompt (CMD):

```cmd
cd "E:\New folder\Telegram Desktop\DeepFake\DeepFake\backend"
venv\Scripts\activate.bat
python scripts/test_face_detection.py image.jpg
```
