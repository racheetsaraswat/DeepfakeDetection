# PowerShell script to activate virtual environment with execution policy workaround
# This script can be run even with restricted execution policy

$ErrorActionPreference = "Stop"

Write-Host "Activating virtual environment..." -ForegroundColor Yellow

# Method 1: Try using the batch file activation (works even with restricted policy)
$batchFile = ".\venv\Scripts\activate.bat"
if (Test-Path $batchFile) {
    Write-Host "Using batch file activation..." -ForegroundColor Cyan
    cmd /c "$batchFile && python --version"
    Write-Host "`nVirtual environment activated!" -ForegroundColor Green
    Write-Host "Note: You're now in a cmd context. Use 'python' directly." -ForegroundColor Yellow
    Write-Host "Example: python scripts/test_face_detection.py image.jpg" -ForegroundColor Cyan
} else {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
}
