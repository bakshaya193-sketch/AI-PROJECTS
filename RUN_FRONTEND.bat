@echo off
REM Frontend Startup Script

cd frontend

REM Check if node_modules exists
if not exist node_modules (
    echo Installing dependencies (first time only)...
    npm install
)

echo.
echo ====================================
echo Starting AI Frontend Server...
echo ====================================
echo.
echo The server is starting...
echo.
echo IMPORTANT:
echo - Keep this window OPEN
echo - Backend must be running in another terminal
echo.
echo Frontend will be at: http://localhost:5173
echo.
echo ====================================
echo.

npm run dev
