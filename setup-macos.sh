#!/bin/bash

# AI Customer Support Agent - macOS/Linux Setup Script
# This script automates the setup process for macOS and Linux users

echo ""
echo "===================================="
echo "AI Customer Support Agent Setup"
echo "===================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python 3 is not installed"
    echo "Please install Python from https://www.python.org/"
    exit 1
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "ERROR: Node.js is not installed"
    echo "Please install Node.js from https://nodejs.org/"
    exit 1
fi

echo "[1/5] Python and Node.js found!"
echo ""

# Navigate to backend and create virtual environment
echo "[2/5] Setting up Python backend..."
cd backend

if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Backend setup complete!"
echo ""
cd ..

# Navigate to frontend and install dependencies
echo "[3/5] Setting up Node.js frontend..."
cd frontend

echo "Installing npm dependencies..."
npm install

echo "Frontend setup complete!"
echo ""
cd ..

# Ask for OpenAI API Key
echo "[4/5] Checking for OpenAI API Key..."
if [ ! -f backend/.env ]; then
    echo "Creating .env file..."
    cp backend/.env.example backend/.env
    echo ""
    echo "=================================="
    echo "IMPORTANT: Add your OpenAI API Key"
    echo "=================================="
    echo ""
    echo "1. Get your API key from: https://platform.openai.com/api-keys"
    echo "2. Open backend/.env in a text editor"
    echo "3. Replace: OPENAI_API_KEY=sk-your-api-key-here"
    echo "4. With your actual API key"
    echo ""
    read -p "Press ENTER after adding your API key..."
else
    echo ".env file already exists!"
fi

echo "[5/5] Setup complete!"
echo ""
echo "===================================="
echo "Next Steps:"
echo "===================================="
echo ""
echo "1. Make sure you added your OpenAI API key to backend/.env"
echo ""
echo "2. Start Backend (Terminal 1):"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   python main.py"
echo ""
echo "3. Start Frontend (Terminal 2):"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo "4. Open browser: http://localhost:5173"
echo ""
echo "5. Upload sample documents from sample-documents/ folder"
echo ""
echo "For more info, see README.md"
echo ""
