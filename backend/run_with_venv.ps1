# Helper script to run Python commands with venv activated
# Usage: .\run_with_venv.ps1 "python scripts/test_face_detection.py image.jpg"

param(
    [Parameter(Mandatory=$true)]
    [string]$Command
)

$ErrorActionPreference = "Stop"

$venvPython = ".\venv\Scripts\python.exe"
if (Test-Path $venvPython) {
    Write-Host "Running with virtual environment Python..." -ForegroundColor Cyan
    & $venvPython -c $Command
} else {
    Write-Host "Virtual environment not found!" -ForegroundColor Red
    exit 1
}
