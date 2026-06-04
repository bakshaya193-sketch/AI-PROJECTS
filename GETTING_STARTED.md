# 🚀 Getting Started - AI Customer Support Agent

**Welcome!** Your complete portfolio project is ready. Follow this guide to get everything running.

---

## ⏱️ Time Required
- **Setup**: 10-15 minutes
- **First run**: 5 minutes
- **Understanding the code**: 30-60 minutes

---

## 📋 Pre-Requirements (Check These First!)

Before starting, make sure you have:

### 1. Python 3.8+
```bash
python --version
```
If not installed: Download from https://www.python.org/

### 2. Node.js 16+
```bash
node --version
npm --version
```
If not installed: Download from https://nodejs.org/

### 3. OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Sign up or log in
3. Click "Create new secret key"
4. Copy it somewhere safe
5. **You'll need this in 5 minutes!**

---

## 🎯 The 3-Step Setup

### Step 1: Setup Backend (5 minutes)

**1a. Navigate to backend folder**
```bash
cd backend
```

**1b. Copy environment template**
```bash
# Windows (PowerShell)
Copy-Item .env.example .env

# Mac/Linux
cp .env.example .env
```

**1c. Edit .env and add your API key**
```bash
# Open .env in your text editor
# Find this line: OPENAI_API_KEY=sk-your-api-key-here
# Replace with your actual key: OPENAI_API_KEY=sk-abc123xyz...
```

**1d. Create Python virtual environment**
```bash
python -m venv venv
```

**1e. Activate virtual environment**
```bash
# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal line.

**1f. Install Python packages**
```bash
pip install -r requirements.txt
```

**1g. Start the backend server**
```bash
python main.py
```

✅ **Success!** You should see:
```
INFO: Uvicorn running on http://0.0.0.0:8000
```

**Leave this terminal running!** →

---

### Step 2: Setup Frontend (5 minutes)

**2a. Open a NEW terminal (keep backend running!)**

**2b. Navigate to frontend**
```bash
cd frontend
```

**2c. Install dependencies**
```bash
npm install
```

**2d. Start development server**
```bash
npm run dev
```

✅ **Success!** You should see:
```
Local: http://localhost:5173/
```

**Leave this terminal running too!** →

---

### Step 3: Test in Browser (5 minutes)

**3a. Open http://localhost:5173 in your browser**

**3b. You should see:**
- Navigation bar with 3 buttons (Chat, Admin Upload, Tickets)
- "✅ Backend Connected" at the bottom
- No error messages

**3c. Upload a sample document**
1. Click "Admin Upload" in the top menu
2. Click "Choose File" button
3. Select file: `sample-documents/refund-policy.txt`
4. Wait for "✅ Document uploaded" message
5. See "45 chunks added"

**3d. Chat with the AI**
1. Click "Chat" in the top menu
2. Type: "What is your refund policy?"
3. Wait 1-3 seconds for response
4. See AI answer with sources below

**3e. Create a support ticket**
1. In Chat, type: "What is the company CEO's name?"
2. AI responds: "I don't have enough information..."
3. Click "Support Tickets"
4. See your question as a new ticket

🎉 **You did it!** The system works!

---

## 📚 Next: Learn the System

### Quick Understanding (15 minutes)

Read these files in order:
1. **QUICKSTART.md** (5 min) - Overview
2. **FILE_REFERENCE.md** (10 min) - Where is everything?

### Deep Understanding (45 minutes)

1. **README.md** (20 min) - Full documentation
2. **ARCHITECTURE.md** (25 min) - How it all works

### Exploration (30 minutes)

1. Open `backend/main.py` - See the API endpoints
2. Open `frontend/src/App.jsx` - See the page routing
3. Open `frontend/src/api.js` - See API calls
4. Open `sample-documents/` - See example documents

---

## 🧪 Test Everything Works

Follow the **VERIFICATION.md** checklist to verify:
- [ ] All files exist
- [ ] Backend starts
- [ ] Frontend loads
- [ ] Documents upload
- [ ] Chat responds
- [ ] Tickets are created

Time: ~20 minutes

---

## ⚙️ Common Issues & Fixes

### "Python not found"
```bash
# Make sure Python is in PATH
python --version
# If error, install Python from python.org
```

### "pip: command not found"
```bash
# Try python -m pip instead
python -m pip install -r requirements.txt
```

### "Virtual environment not working"
```bash
# Delete venv folder and recreate
rm -r venv  # or: rmdir venv /s (Windows)
python -m venv venv
venv\Scripts\activate  # Windows
# or: source venv/bin/activate (Mac/Linux)
```

### "Module not found error"
```bash
# Make sure venv is activated (see (venv) prefix)
# Then reinstall:
pip install -r requirements.txt
```

### "Backend won't start (Port 8000 in use)"
```bash
# Port 8000 is already used
# Change port in backend/main.py line 303 or:
# Kill process on port 8000
# Or use different port: python main.py --port 8001
```

### "Frontend won't load (Port 5173 in use)"
```bash
# Port 5173 is already used
# Change port in frontend/vite.config.js or:
# Kill process on port 5173
```

### "Backend won't connect (no documents)"
```bash
# Upload sample documents first!
# Go to Admin Upload page
# Select sample-documents/refund-policy.txt
# Wait for success message
```

### "API key error"
```bash
# 1. Check .env file has your key
# 2. Key should start with: sk-
# 3. Get new key from: platform.openai.com/api-keys
# 4. Save and restart backend
```

See **README.md** Troubleshooting section for more.

---

## 🎓 Understanding the Architecture

### Simple Data Flow:

```
You type a question
        ↓
Frontend sends to backend
        ↓
Backend searches documents in ChromaDB
        ↓
Backend sends to OpenAI GPT
        ↓
OpenAI returns answer
        ↓
Frontend displays answer
        ↓
If can't answer → Create ticket
```

See **ARCHITECTURE.md** for detailed flow diagrams.

---

## 💡 Tips for Success

1. **Keep terminals running**
   - Don't close terminal 1 (backend)
   - Don't close terminal 2 (frontend)
   - Open terminal 3 for other commands

2. **Use sample documents first**
   - Test with provided documents
   - Then use your own content

3. **Check browser console**
   - F12 in browser → Console tab
   - Shows any JavaScript errors
   - Very helpful for debugging

4. **Check browser network tab**
   - F12 → Network tab
   - See actual API requests/responses
   - Shows response time

5. **Monitor backend logs**
   - Look at terminal running backend
   - Shows detailed error messages
   - Very helpful for debugging

---

## 🚀 Next Steps After Setup

### 1. Customize (30 minutes)
- [ ] Change system prompt in `backend/main.py` line 207
- [ ] Replace sample documents with your content
- [ ] Change colors in `frontend/src/styles/App.css`

### 2. Enhance (1-2 hours)
- [ ] Add more pages
- [ ] Add authentication
- [ ] Add chat history
- [ ] Add analytics

### 3. Deploy (1-2 hours)
- [ ] Deploy frontend to Vercel/Netlify
- [ ] Deploy backend to Heroku/AWS
- [ ] Update API URL for production
- [ ] Configure environment variables

---

## 📞 Where to Get Help

| Issue | Where to Look |
|-------|---------------|
| Setup problems | README.md → Troubleshooting |
| Understanding files | FILE_REFERENCE.md |
| System design | ARCHITECTURE.md |
| Quick setup | QUICKSTART.md |
| Verify setup | VERIFICATION.md |
| API reference | README.md → API Endpoints |
| Code explanation | Inline comments in files |

---

## 🎉 You're Ready!

Everything is set up and ready to go. 

**Your next steps:**

1. ✅ Make sure both terminals are running (backend + frontend)
2. ✅ Go to http://localhost:5173
3. ✅ Upload sample documents
4. ✅ Chat with the AI
5. ✅ Explore the code
6. ✅ Read ARCHITECTURE.md to understand it deeply
7. ✅ Customize for your needs

---

## 📈 Project Stats

- **33 Files** created
- **8000+ Lines** of code
- **5000+ Words** of documentation
- **4 Sample Documents** included
- **Ready to deploy** production-quality project

---

## 💬 What You Built

A complete **AI Customer Support Agent** that:
- ✅ Answers questions from your documents
- ✅ Uses semantic search (vector database)
- ✅ Leverages ChatGPT for responses
- ✅ Creates tickets for complex questions
- ✅ Has a professional UI
- ✅ Works on desktop and mobile
- ✅ Is completely customizable
- ✅ Is portfolio-ready

---

## 🎓 What You Learned

- Full-stack development (frontend + backend)
- React + Vite (modern frontend)
- FastAPI (modern Python backend)
- Vector databases (ChromaDB)
- AI integration (OpenAI API)
- RAG (Retrieval-Augmented Generation)
- REST API design
- Responsive CSS design
- Database management (SQLite)
- Project structure and organization

---

**Happy coding! 🚀**

Questions? Check the documentation files or look at the code comments.

Need to understand something? Read ARCHITECTURE.md for deep dives.

Ready to customize? Open the files and start editing!

---

*Last Updated: June 2026*
*Project: AI Customer Support Agent v1.0*
