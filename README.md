# AI Customer Support Agent 🤖

A complete full-stack intelligent customer support chatbot that answers customer questions using uploaded company documents powered by OpenAI, ChromaDB, and RAG (Retrieval-Augmented Generation).

## 🌟 Features

- **AI-Powered Chat**: Uses OpenAI GPT to answer customer questions
- **Document Upload**: Upload PDF and TXT files to train the AI
- **Semantic Search**: ChromaDB retrieves relevant document chunks
- **Smart Ticket System**: Automatically creates support tickets for unanswered questions
- **Admin Panel**: Easy document management interface
- **Responsive Design**: Works on desktop, tablet, and mobile devices
- **Source Citations**: Shows which documents were used for answers
- **SQLite Database**: Stores support tickets for your team

## 🏗️ Project Structure

```
ai-customer-support-agent/
├── backend/                    # FastAPI Backend
│   ├── main.py                # Main FastAPI application
│   ├── database.py            # SQLite database initialization
│   ├── utils.py               # Text extraction and chunking utilities
│   ├── requirements.txt        # Python dependencies
│   ├── .env.example           # Environment variables template
│   └── .env                   # (Create this - your API keys)
│
├── frontend/                   # React + Vite Frontend
│   ├── src/
│   │   ├── components/        # Reusable React components
│   │   │   ├── ChatBox.jsx
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── UploadDocument.jsx
│   │   │   └── Navigation.jsx
│   │   ├── pages/             # Page components
│   │   │   ├── ChatPage.jsx
│   │   │   ├── AdminPage.jsx
│   │   │   └── TicketsPage.jsx
│   │   ├── styles/            # CSS stylesheets
│   │   │   ├── App.css
│   │   │   ├── ChatPage.css
│   │   │   ├── AdminPage.css
│   │   │   └── TicketsPage.css
│   │   ├── api.js             # API service layer
│   │   ├── App.jsx            # Main App component
│   │   └── main.jsx           # Entry point
│   ├── index.html             # HTML template
│   ├── package.json           # NPM dependencies
│   └── vite.config.js         # Vite configuration
│
├── sample-documents/           # Sample documents for testing
│   ├── refund-policy.txt
│   ├── shipping-policy.txt
│   ├── password-reset-guide.txt
│   └── pricing-faq.txt
│
└── README.md                  # This file
```

## 🚀 Quick Start

### Prerequisites

Before you begin, make sure you have installed:
- **Node.js** (v16+) - [Download](https://nodejs.org/)
- **Python** (v3.8+) - [Download](https://www.python.org/)
- **OpenAI API Key** - [Get one here](https://platform.openai.com/api-keys)

### Step 1: Get Your OpenAI API Key

1. Go to [https://platform.openai.com/api-keys](https://platform.openai.com/api-keys)
2. Sign up or log in to your OpenAI account
3. Click "Create new secret key"
4. Copy your API key (you won't be able to see it again!)
5. Keep it safe - don't commit it to version control

### Step 2: Setup Backend

#### 2.1 Navigate to Backend Directory

```bash
cd backend
```

#### 2.2 Create Environment File

Copy `.env.example` to `.env` and add your OpenAI API key:

```bash
# On Windows (PowerShell)
Copy-Item .env.example .env

# On Windows (Command Prompt)
copy .env.example .env

# On Mac/Linux
cp .env.example .env
```

Then open `.env` in your text editor and replace:
```
OPENAI_API_KEY=sk-your-api-key-here
```

With your actual OpenAI API key:
```
OPENAI_API_KEY=sk-proj-abc123xyz789...
```

#### 2.3 Create Virtual Environment

```bash
# On Windows
python -m venv venv
venv\Scripts\activate

# On Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

#### 2.4 Install Python Dependencies

```bash
pip install -r requirements.txt
```

#### 2.5 Run Backend Server

```bash
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

The backend is now running! Open [http://localhost:8000](http://localhost:8000) in your browser to see the API.

### Step 3: Setup Frontend

#### 3.1 Open New Terminal/Command Prompt

Open a new terminal window **while keeping the backend running**.

#### 3.2 Navigate to Frontend Directory

```bash
cd frontend
```

#### 3.3 Install Dependencies

```bash
npm install
```

#### 3.4 Run Frontend Server

```bash
npm run dev
```

You should see:
```
  VITE v5.0.0  ready in 123 ms

  ➜  Local:   http://localhost:5173/
```

#### 3.5 Open in Browser

Click the link or navigate to [http://localhost:5173](http://localhost:5173)

## 💻 Using the Application

### 1. Upload Documents (Admin Page)

1. Click **"Admin Upload"** in the navigation
2. Click **"Choose File"** button
3. Select a PDF or TXT file (try sample documents first)
4. Wait for success message
5. Repeat for multiple documents

**Recommended**: Upload all sample documents from `/sample-documents/` folder first.

### 2. Chat with AI (Chat Page)

1. Click **"Chat"** in the navigation
2. Type a question about the uploaded documents
3. Wait for AI response
4. View source documents in the response

**Example Questions**:
- "What is your refund policy?"
- "How long does shipping take?"
- "How do I reset my password?"
- "What pricing plans do you offer?"

### 3. View Support Tickets (Tickets Page)

1. Click **"Support Tickets"** in the navigation
2. View all unresolved customer questions
3. Click refresh to get latest tickets
4. Tickets auto-update every 30 seconds

## 🔧 Backend API Endpoints

### Health Check
```
GET /health
Response: { "status": "healthy" }
```

### Upload Document
```
POST /upload
Headers: Content-Type: multipart/form-data
Body: file (PDF or TXT)

Response: {
  "message": "Document 'filename.pdf' uploaded successfully",
  "file_name": "filename.pdf",
  "chunks_added": 45
}
```

### Chat with AI
```
POST /chat
Headers: Content-Type: application/json
Body: { "question": "Your question here" }

Response: {
  "answer": "AI response...",
  "sources": ["document.pdf"],
  "ticket_created": false,
  "ticket_id": null
}
```

### Get Tickets
```
GET /tickets
Response: [
  {
    "id": 1,
    "question": "Customer question...",
    "status": "unresolved",
    "created_date": "2024-01-15T10:30:00"
  }
]
```

## 📁 Sample Documents

The project includes 4 sample documents for testing:

1. **refund-policy.txt** - Company refund policy and procedures
2. **shipping-policy.txt** - Shipping options and delivery times
3. **password-reset-guide.txt** - Password reset instructions
4. **pricing-faq.txt** - Pricing tiers and frequently asked questions

### How to Use Sample Documents

1. Go to **Admin Upload** page
2. Upload each file from `sample-documents/` folder
3. You'll see "✅ Document uploaded" confirmation
4. Go to **Chat** page
5. Ask questions like:
   - "How much is shipping?"
   - "Can I get a refund?"
   - "What payment methods do you accept?"

## 🗄️ Database

The application uses SQLite to store support tickets.

### Database File
- **Location**: `backend/support_tickets.db`
- **Created automatically** on first run
- **Tables**: `tickets` with columns:
  - `id` - Unique ticket ID
  - `question` - Customer question
  - `status` - 'unresolved' or 'resolved'
  - `created_date` - ISO format timestamp
  - `resolved_date` - Optional resolution timestamp

## 🔐 Environment Variables

### Backend (.env file)

```bash
# Required: Your OpenAI API Key
OPENAI_API_KEY=sk-your-key-here
```

### Frontend

Frontend uses API at `http://localhost:8000` (hardcoded for local development).

To change it, edit `frontend/src/api.js`:
```javascript
const API_BASE_URL = 'http://localhost:8000';
```

## 🐛 Troubleshooting

### Backend Won't Start

**Error**: `ModuleNotFoundError: No module named 'fastapi'`

**Solution**:
```bash
# Make sure virtual environment is activated
# On Windows: venv\Scripts\activate
# On Mac/Linux: source venv/bin/activate

# Then reinstall requirements
pip install -r requirements.txt
```

### Frontend Won't Connect to Backend

**Error**: `Backend server not connected` warning

**Solutions**:
1. Make sure backend is running: `python main.py` in backend folder
2. Backend must run on `http://localhost:8000`
3. Check if port 8000 is already in use
4. Check browser console for CORS errors

### CORS Error

**Error**: `CORS policy: No 'Access-Control-Allow-Origin' header`

**Solution**: This is normal for local development. Backend has CORS enabled for localhost:5173.

### File Upload Fails

**Error**: `Only PDF and TXT files are supported`

**Solutions**:
1. Check file format (must be .pdf or .txt)
2. File size should be under 10MB
3. Try with sample documents first

### No Response from AI

**Error**: AI doesn't respond to questions

**Possible Causes**:
1. No documents uploaded yet - upload sample documents first
2. OpenAI API key is invalid - check your `.env` file
3. OpenAI API quota exceeded - check your usage on platform.openai.com
4. Network error - check internet connection

## 📦 Dependencies

### Backend (Python)
- **fastapi** - Web framework
- **uvicorn** - ASGI server
- **openai** - OpenAI API client
- **chromadb** - Vector database
- **PyPDF2** - PDF text extraction
- **pydantic** - Data validation
- **python-dotenv** - Environment variables
- **python-multipart** - File upload support

### Frontend (JavaScript)
- **react** - UI library
- **react-dom** - React DOM rendering
- **axios** - HTTP client
- **vite** - Build tool

## 🎨 UI/UX Features

- **Dark Mode Ready**: Uses CSS variables for easy theming
- **Responsive Design**: Works on desktop, tablet, and mobile
- **Real-time Updates**: Auto-refresh for tickets every 30 seconds
- **Loading States**: Visual feedback during API calls
- **Error Handling**: User-friendly error messages
- **Smooth Animations**: Transitions and floading effects
- **Accessibility**: Semantic HTML and keyboard navigation

## 🚀 Production Deployment

### Backend Deployment (Vercel, Heroku, AWS)

1. Create `requirements.txt` (already done)
2. Set environment variables on hosting platform
3. Deploy with:
   ```bash
   # Heroku example
   git push heroku main
   ```

### Frontend Deployment (Vercel, Netlify, GitHub Pages)

1. Build production bundle:
   ```bash
   npm run build
   ```
2. Deploy `dist/` folder to hosting
3. Update API URL in `frontend/src/api.js` to match backend

## 📝 How It Works

### RAG (Retrieval-Augmented Generation) Pipeline

1. **Document Upload**
   - User uploads PDF/TXT file
   - Text is extracted and split into chunks
   - Chunks are embedded and stored in ChromaDB

2. **Query Processing**
   - Customer asks a question
   - Question is embedded using OpenAI
   - ChromaDB retrieves top 3 most relevant chunks

3. **AI Response**
   - Retrieved chunks + system prompt + question sent to GPT
   - GPT generates context-aware answer
   - Response includes source documents

4. **Ticket Creation**
   - If AI says "don't have enough information"
   - Support ticket is created automatically
   - Ticket appears in Tickets page for team

## 💡 Tips

### For Best Results

1. **Upload Quality Documents**: Clear, well-formatted documents work best
2. **Be Specific**: Ask specific questions with details
3. **Use Multiple Documents**: Upload various related documents for better coverage
4. **Check Sources**: Review which documents were used for the answer
5. **Iterate**: Refine documents based on customer questions

### Performance

- Vector search is fast (<100ms)
- GPT response typically takes 1-3 seconds
- Chunks are limited to 500 characters with 100 char overlap

## 🤝 Contributing

To improve this project:

1. Add more document types
2. Implement document version control
3. Add admin dashboard for analytics
4. Implement conversation history
5. Add multi-language support

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Check console for error messages
3. Verify all services are running
4. Check API responses in browser network tab

## 📄 License

This project is provided as-is for educational and commercial use.

## 🎓 Learning Resources

- **FastAPI**: [https://fastapi.tiangolo.com/](https://fastapi.tiangolo.com/)
- **React**: [https://react.dev/](https://react.dev/)
- **ChromaDB**: [https://docs.trychroma.com/](https://docs.trychroma.com/)
- **OpenAI API**: [https://platform.openai.com/docs/](https://platform.openai.com/docs/)

## 🎉 Getting Started Checklist

- [ ] Install Node.js and Python
- [ ] Get OpenAI API key
- [ ] Set up `.env` file with API key
- [ ] Install backend dependencies (`pip install -r requirements.txt`)
- [ ] Run backend server (`python main.py`)
- [ ] Install frontend dependencies (`npm install`)
- [ ] Run frontend server (`npm run dev`)
- [ ] Upload sample documents from `sample-documents/` folder
- [ ] Test chat functionality
- [ ] View support tickets

---

**Built with ❤️ using React, FastAPI, and OpenAI**
