@echo off
REM Automated Installation Script for AI Customer Support Agent
REM This script will do everything for you!

echo.
echo ====================================
echo AI Customer Support Agent
echo Complete Automated Setup
echo ====================================
echo.

REM Step 1: Navigate to backend
cd backend

echo [1/5] Creating Python virtual environment...
if not exist venv (
    python -m venv venv
    echo Virtual environment created!
) else (
    echo Virtual environment already exists, skipping...
)

echo [2/5] Activating virtual environment...
call venv\Scripts\activate.bat

echo [3/5] Upgrading pip (this fixes the C++ issue)...
python -m pip install --upgrade pip setuptools wheel

echo [4/5] Installing Python packages...
echo This may take 2-3 minutes, please wait...
pip install -r requirements.txt

echo [5/5] Installation complete!
echo.
echo ====================================
echo SUCCESS! Everything installed
echo ====================================
echo.
echo NEXT STEPS:
echo.
echo 1. Double-click: RUN_BACKEND.bat (in main folder)
echo    This starts the backend server
echo.
echo 2. Open NEW terminal and double-click: RUN_FRONTEND.bat
echo    This starts the frontend
echo.
echo 3. Open browser: http://localhost:5173
echo.
echo ====================================
echo.
echo Installation complete! You can close this window now.
echo.
