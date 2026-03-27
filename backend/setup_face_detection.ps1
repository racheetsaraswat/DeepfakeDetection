# PowerShell script to install face detection dependencies
# Run this from the backend directory

Write-Host "Setting up face detection dependencies..." -ForegroundColor Green

# Check if venv exists
if (Test-Path ".\venv\Scripts\Activate.ps1") {
    Write-Host "Activating virtual environment..." -ForegroundColor Yellow
    .\venv\Scripts\Activate.ps1
    
    # Check Python
    $pythonVersion = python --version 2>&1
    Write-Host "Python: $pythonVersion" -ForegroundColor Cyan
    
    # Upgrade pip
    Write-Host "Upgrading pip..." -ForegroundColor Yellow
    python -m pip install --upgrade pip
    
    # Install face detection dependencies
    Write-Host "Installing face detection dependencies..." -ForegroundColor Yellow
    pip install mtcnn facenet-pytorch
    
    # Verify installation
    Write-Host "`nVerifying installation..." -ForegroundColor Yellow
    python -c "import cv2; print('OpenCV:', cv2.__version__)" 2>&1
    python -c "import mtcnn; print('MTCNN: OK')" 2>&1
    
    Write-Host "`nSetup complete! You can now test face detection." -ForegroundColor Green
    Write-Host "Test with: python scripts/test_face_detection.py path/to/image.jpg" -ForegroundColor Cyan
} else {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    Write-Host "Please create a virtual environment first:" -ForegroundColor Yellow
    Write-Host "  python -m venv venv" -ForegroundColor White
    Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
    Write-Host "  pip install -r requirements.txt" -ForegroundColor White
}
