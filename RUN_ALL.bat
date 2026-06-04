@echo off
title AI Customer Support Agent - Auto Setup and Run

echo.
echo ============================================
echo  AI Customer Support Agent - Auto Setup
echo ============================================
echo.

REM ---- BACKEND SETUP ----
echo [Step 1/5] Activating Python virtual environment...
cd backend
call venv\Scripts\activate.bat

echo [Step 2/5] Installing all required packages...
pip install fastapi==0.115.0 pydantic==2.7.0 uvicorn python-dotenv openai chromadb PyPDF2 python-multipart deep-translator langdetect textblob nltk python-jose passlib[bcrypt] Pillow requests aiofiles --quiet

echo [Step 3/5] Installing NLTK data for sentiment analysis...
python -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('averaged_perceptron_tagger', quiet=True); nltk.download('brown', quiet=True); print('NLTK data ready')"

echo [Step 4/5] Starting Backend Server...
echo.
echo Backend will start on http://localhost:8000
echo.
echo ============================================
echo  IMPORTANT: Keep this window OPEN!
echo  Now open a NEW terminal and run:
echo  cd frontend
echo  npm install
echo  npm run dev
echo ============================================
echo.

REM Start backend
python main.py

pause
