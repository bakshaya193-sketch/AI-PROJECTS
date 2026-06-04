@echo off
REM AI Customer Support Agent - Windows Setup Script
REM This script automates the setup process for Windows users

echo.
echo ====================================
echo AI Customer Support Agent Setup
echo ====================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)

REM Check if Node.js is installed
node --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Node.js is not installed or not in PATH
    echo Please install Node.js from https://nodejs.org/
    pause
    exit /b 1
)

echo [1/5] Python and Node.js found!
echo.

REM Navigate to backend and create virtual environment
echo [2/5] Setting up Python backend...
cd backend

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
)

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing Python dependencies...
pip install -r requirements.txt

echo Backend setup complete!
echo.
cd ..

REM Navigate to frontend and install dependencies
echo [3/5] Setting up Node.js frontend...
cd frontend

echo Installing npm dependencies...
call npm install

echo Frontend setup complete!
echo.
cd ..

REM Ask for OpenAI API Key
echo [4/5] Checking for OpenAI API Key...
if not exist backend\.env (
    echo Creating .env file...
    copy backend\.env.example backend\.env
    echo.
    echo ==================================
    echo IMPORTANT: Add your OpenAI API Key
    echo ==================================
    echo.
    echo 1. Get your API key from: https://platform.openai.com/api-keys
    echo 2. Open backend\.env in a text editor
    echo 3. Replace: OPENAI_API_KEY=sk-your-api-key-here
    echo 4. With your actual API key
    echo.
    pause
) else (
    echo .env file already exists!
)

echo [5/5] Setup complete!
echo.
echo ====================================
echo Next Steps:
echo ====================================
echo.
echo 1. Make sure you added your OpenAI API key to backend\.env
echo.
echo 2. Start Backend (Terminal 1):
echo    cd backend
echo    venv\Scripts\activate
echo    python main.py
echo.
echo 3. Start Frontend (Terminal 2):
echo    cd frontend
echo    npm run dev
echo.
echo 4. Open browser: http://localhost:5173
echo.
echo 5. Upload sample documents from sample-documents\ folder
echo.
echo For more info, see README.md
echo.
pause
