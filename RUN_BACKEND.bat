@echo off
REM Backend Startup Script - Keeps running!

cd backend

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Start the backend server
echo.
echo ====================================
echo Starting AI Backend Server...
echo ====================================
echo.
echo The server is now running!
echo.
echo Keep this window OPEN!
echo.
echo Backend running on: http://localhost:8000
echo.
echo Next: Open NEW terminal and run:
echo   cd frontend
echo   npm install
echo   npm run dev
echo.
echo Then open browser: http://localhost:5173
echo.
echo ====================================
echo.

python main.py
