@echo off
REM Batch script to install face detection dependencies
REM Run this from the backend directory

echo Setting up face detection dependencies...

if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
    
    echo Installing face detection dependencies...
    pip install mtcnn facenet-pytorch
    
    echo.
    echo Verifying installation...
    python -c "import cv2; print('OpenCV:', cv2.__version__)"
    python -c "import mtcnn; print('MTCNN: OK')"
    
    echo.
    echo Setup complete! You can now test face detection.
    echo Test with: python scripts/test_face_detection.py path/to/image.jpg
) else (
    echo Virtual environment not found!
    echo Please create a virtual environment first:
    echo   python -m venv venv
    echo   venv\Scripts\activate.bat
    echo   pip install -r requirements.txt
)

pause
