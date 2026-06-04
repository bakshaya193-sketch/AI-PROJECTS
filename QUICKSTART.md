# 🚀 Quick Start Guide

Get your AI Customer Support Agent running in 5 minutes!

## Before You Start

1. **Get OpenAI API Key** → Go to https://platform.openai.com/api-keys and create one
2. **Install Node.js** → Download from https://nodejs.org/ (v16+)
3. **Install Python** → Download from https://www.python.org/ (v3.8+)

---

## Step 1: Setup Backend (Terminal 1)

```bash
# Navigate to backend folder
cd backend

# Create .env file with your OpenAI key
# Windows (PowerShell):
Copy-Item .env.example .env
# Then edit .env and paste your API key

# Or Mac/Linux:
cp .env.example .env
nano .env  # paste your API key

# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start backend server
python main.py
```

✅ You should see: `INFO: Uvicorn running on http://0.0.0.0:8000`

---

## Step 2: Setup Frontend (Terminal 2 - Keep Terminal 1 Running!)

```bash
# Open new terminal, navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

✅ You should see: `Local: http://localhost:5173/`

---

## Step 3: Open in Browser

1. Go to [http://localhost:5173](http://localhost:5173)
2. Click **"Admin Upload"** in the top menu
3. Upload files from `sample-documents/` folder
4. Click **"Chat"** and test with questions:
   - "What's your refund policy?"
   - "How long does shipping take?"
   - "How do I reset my password?"

---

## ⚡ Terminal Commands Summary

### Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # or: source venv/bin/activate
pip install -r requirements.txt
python main.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 🎯 Test the Complete Flow

1. **Upload Document**
   - Go to Admin Upload page
   - Click "Choose File"
   - Select `sample-documents/pricing-faq.txt`
   - See "✅ Document uploaded" message

2. **Ask a Question**
   - Go to Chat page
   - Type: "How much does the basic plan cost?"
   - See AI response with sources

3. **Create a Ticket**
   - Ask something not in documents: "What's your CEO's name?"
   - AI creates support ticket automatically
   - Go to Tickets page to see it

---

## ❌ Something Not Working?

### Backend won't start
```
Error: ModuleNotFoundError
→ Make sure venv is activated: venv\Scripts\activate
→ Then run: pip install -r requirements.txt
```

### Frontend won't load
```
Error: Connection refused
→ Backend must be running on port 8000
→ Run: python main.py in backend folder
```

### File upload fails
```
Error: Only PDF and TXT files supported
→ Use files from sample-documents/ folder
→ Or create your own .txt file
```

### AI doesn't respond
```
Error: Empty response
→ Upload sample documents first
→ Check your OpenAI API key in .env
→ Make sure you have API credits
```

---

## 📱 Browser URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

---

## 🎓 Next Steps

1. ✅ Customize sample documents with your company info
2. ✅ Update system prompt in `backend/main.py` line 207
3. ✅ Customize styling in `frontend/src/styles/`
4. ✅ Deploy to production (Vercel, Heroku, AWS)

---

## 📚 Full Documentation

See `README.md` for complete documentation, API reference, and troubleshooting.

---

**Need Help?** Check the README.md for detailed troubleshooting guide.
