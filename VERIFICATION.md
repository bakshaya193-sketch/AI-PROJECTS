# ✅ Setup Verification Checklist

Use this checklist to verify your complete setup is working correctly.

## Pre-Setup Requirements

- [ ] Python 3.8+ installed (`python --version`)
- [ ] Node.js v16+ installed (`node --version`)
- [ ] OpenAI API key obtained from https://platform.openai.com/api-keys
- [ ] Text editor installed (VSCode, Sublime, etc.)

## Backend Setup Verification

### File Structure
- [ ] `backend/main.py` exists
- [ ] `backend/database.py` exists
- [ ] `backend/utils.py` exists
- [ ] `backend/requirements.txt` exists
- [ ] `backend/.env` file created (not just .env.example)

### Environment Setup
```bash
# In backend folder, check:
cd backend
```
- [ ] Virtual environment created: `venv/` folder exists
- [ ] Virtual environment activated: your terminal shows `(venv)` prefix
- [ ] OpenAI key in `.env` file: `OPENAI_API_KEY=sk-...`

### Dependencies
```bash
# While in venv:
pip list
```
- [ ] fastapi==0.104.1 installed
- [ ] uvicorn==0.24.0 installed
- [ ] openai==0.27.8 installed
- [ ] chromadb==0.3.21 installed
- [ ] PyPDF2==3.0.1 installed

### Backend Server
```bash
python main.py
```
- [ ] Server starts without errors
- [ ] Output shows: `INFO: Uvicorn running on http://0.0.0.0:8000`
- [ ] No `ModuleNotFoundError` or `ImportError`

### API Endpoints
Open browser and go to:
- [ ] http://localhost:8000 - Shows API info ✅
- [ ] http://localhost:8000/health - Shows {"status": "healthy"} ✅
- [ ] http://localhost:8000/docs - Shows interactive API docs ✅

## Frontend Setup Verification

### File Structure
```bash
cd frontend
```
- [ ] `package.json` exists
- [ ] `vite.config.js` exists
- [ ] `index.html` exists
- [ ] `src/main.jsx` exists
- [ ] `src/App.jsx` exists
- [ ] `src/api.js` exists
- [ ] `src/components/` folder with 4 components
- [ ] `src/pages/` folder with 3 pages
- [ ] `src/styles/` folder with 4 CSS files

### Dependencies
```bash
cd frontend
npm list
```
- [ ] react@18.2.0 installed
- [ ] react-dom@18.2.0 installed
- [ ] axios@1.6.0 installed
- [ ] vite@5.0.0 installed

### Development Server
```bash
npm run dev
```
- [ ] Server starts without errors
- [ ] Output shows: `Local: http://localhost:5173/`
- [ ] No build errors

### Browser Access
Open http://localhost:5173 in browser:
- [ ] Page loads without errors
- [ ] Navigation bar visible (Chat, Admin Upload, Tickets)
- [ ] "Backend Connected" status shown ✅
- [ ] No red error messages

## Sample Documents Verification

### Files Exist
- [ ] `sample-documents/refund-policy.txt` exists
- [ ] `sample-documents/shipping-policy.txt` exists
- [ ] `sample-documents/password-reset-guide.txt` exists
- [ ] `sample-documents/pricing-faq.txt` exists

### File Contents
```bash
# Check file sizes (should be > 1KB)
cd sample-documents
ls -la  # or: dir on Windows
```
- [ ] refund-policy.txt > 1KB
- [ ] shipping-policy.txt > 1KB
- [ ] password-reset-guide.txt > 1KB
- [ ] pricing-faq.txt > 1KB

## Complete Workflow Test

### Step 1: Upload Document
- [ ] Go to http://localhost:5173 in browser
- [ ] Click "Admin Upload" button
- [ ] Click "Choose File"
- [ ] Select `sample-documents/refund-policy.txt`
- [ ] See "✅ Document uploaded" message
- [ ] Shows chunk count (e.g., "45 chunks added")

### Step 2: Chat with AI
- [ ] Click "Chat" button in navigation
- [ ] See empty state with "Welcome to AI Support!"
- [ ] Type: "What is your refund policy?"
- [ ] Wait for AI response (1-3 seconds)
- [ ] See answer in message bubble
- [ ] See "Sources: refund-policy.txt" below answer

### Step 3: View Tickets
- [ ] Click "Support Tickets" button
- [ ] See message: "No Tickets" (nothing uploaded yet that would trigger)
- [ ] Upload `sample-documents/pricing-faq.txt`
- [ ] Go to Chat
- [ ] Ask: "Who is your CEO?" (not in documents)
- [ ] AI should say "don't have enough information"
- [ ] Go to Tickets page
- [ ] See new ticket created
- [ ] Ticket shows your question

### Step 4: Multiple Documents
- [ ] Upload all 4 sample documents
- [ ] Ask varied questions:
  - "How much is shipping?" → Uses shipping-policy.txt
  - "How do I reset my password?" → Uses password-reset-guide.txt
  - "What pricing plans exist?" → Uses pricing-faq.txt
- [ ] Each response should cite the correct source

## Database Verification

### SQLite Database
```bash
# Check if database file was created
cd backend
dir support_tickets.db  # or ls support_tickets.db on Mac/Linux
```
- [ ] File `support_tickets.db` exists after running backend
- [ ] File size > 0 bytes
- [ ] No permission errors

### Table Verification
```bash
# If you have SQLite CLI installed:
sqlite3 support_tickets.db
> SELECT COUNT(*) FROM tickets;
```
- [ ] Table exists without errors
- [ ] Can run SELECT query
- [ ] Tickets increase when support is triggered

## Vector Database Verification

### ChromaDB Persistence
```bash
cd backend
ls -la chroma_data  # or: dir chroma_data
```
- [ ] Folder `chroma_data/` created
- [ ] Contains database files
- [ ] Grows as documents are uploaded

### Retrieval Test
When you search in chat:
- [ ] Relevant documents are returned quickly (<100ms)
- [ ] Top 3 results show in sources
- [ ] Results match document content

## API Verification

### POST /upload
```bash
# Terminal with curl (or use Postman):
curl -X POST http://localhost:8000/upload \
  -F "file=@sample-documents/refund-policy.txt"

# Should return:
# {"message": "Document uploaded successfully", ...}
```
- [ ] Returns 200 status code
- [ ] Shows chunk count
- [ ] No file type errors

### POST /chat
```bash
# Terminal with curl:
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"question": "What is your refund policy?"}'

# Should return:
# {"answer": "...", "sources": [...], ...}
```
- [ ] Returns 200 status code
- [ ] Answer contains meaningful response
- [ ] Sources array is populated
- [ ] No API key errors

### GET /tickets
```bash
# Terminal:
curl http://localhost:8000/tickets

# Should return array of tickets:
# [{"id": 1, "question": "...", ...}, ...]
```
- [ ] Returns 200 status code
- [ ] Returns JSON array
- [ ] Tickets created are listed

## Performance Verification

### Response Times
- [ ] File upload: <5 seconds
- [ ] Document indexing: <2 seconds
- [ ] AI response: 1-3 seconds
- [ ] Ticket creation: <1 second

### No Errors In:
- [ ] Browser console (F12 → Console tab)
- [ ] Browser network tab (F12 → Network tab)
- [ ] Backend terminal output
- [ ] Frontend terminal output

## Security Verification

- [ ] `.env` file is in `.gitignore` ✅
- [ ] API key not visible in code
- [ ] API key not in localStorage (browser storage)
- [ ] No sensitive data in console logs
- [ ] CORS working (allows localhost:5173)

## Documentation Verification

- [ ] `README.md` is complete and readable
- [ ] `QUICKSTART.md` has clear instructions
- [ ] `ARCHITECTURE.md` explains system design
- [ ] This `VERIFICATION.md` is helpful

## Troubleshooting

### Backend Issues
If backend won't start:
1. [ ] Check Python version: `python --version`
2. [ ] Check venv is activated
3. [ ] Run: `pip install -r requirements.txt` again
4. [ ] Check `.env` file exists with API key
5. [ ] Check port 8000 isn't used: `netstat -an | grep 8000`

### Frontend Issues
If frontend won't load:
1. [ ] Check Node.js version: `node --version`
2. [ ] Delete `node_modules` and `package-lock.json`
3. [ ] Run: `npm install` again
4. [ ] Check backend is running on port 8000
5. [ ] Check port 5173 isn't used

### API Connection
If can't connect to backend:
1. [ ] Backend running? (Check terminal)
2. [ ] Correct port 8000?
3. [ ] Check firewall isn't blocking
4. [ ] Check network tab in browser DevTools
5. [ ] Try accessing http://localhost:8000 directly

### OpenAI API Errors
If getting OpenAI errors:
1. [ ] Check API key is valid
2. [ ] Check key in `.env` starts with `sk-`
3. [ ] Check account has API credit
4. [ ] Check API key isn't revoked
5. [ ] Check token limits aren't exceeded

## Final Checklist

- [ ] All files created successfully
- [ ] Backend server running
- [ ] Frontend server running
- [ ] Can upload documents
- [ ] Can ask questions
- [ ] Get AI responses
- [ ] Support tickets created
- [ ] No major errors
- [ ] Performance is acceptable
- [ ] Documentation is clear

---

## ✅ Ready to Deploy?

If you checked all boxes, your system is ready!

**Next steps**:
1. Customize sample documents with your content
2. Update system prompt in `backend/main.py`
3. Test with your real company documents
4. Deploy frontend to Vercel/Netlify
5. Deploy backend to Heroku/AWS

See `README.md` and `ARCHITECTURE.md` for details.

---

**Having issues?** Review the Troubleshooting section in `README.md`
