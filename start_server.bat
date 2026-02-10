@echo off
echo ========================================
echo   AI-NutriCurator Backend Server
echo ========================================
echo.

echo [1/2] Checking Python installation...
python --version
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    pause
    exit /b 1
)
echo.

echo [2/2] Starting FastAPI server...
echo Server will run on http://localhost:8000
echo Press Ctrl+C to stop the server
echo.
echo API Documentation: http://localhost:8000/docs
echo.

cd backend
python app.py

pause
