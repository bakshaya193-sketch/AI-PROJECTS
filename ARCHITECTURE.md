# 🏗️ System Architecture

## Overview

The AI Customer Support Agent is a full-stack application that combines RAG (Retrieval-Augmented Generation), semantic search, and AI language models to create an intelligent customer support system.

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    User Browser (React)                     │
│  ┌──────────────┬──────────────┬──────────────────────────┐ │
│  │   ChatPage   │  AdminPage   │    TicketsPage          │ │
│  └──────────────┴──────────────┴──────────────────────────┘ │
└──────────────────────────────────────────────────────────────┘
                              ↓ (HTTP/API)
┌──────────────────────────────────────────────────────────────┐
│                  FastAPI Backend (Python)                   │
│  ┌────────────┐  ┌─────────────┐  ┌─────────────────────┐  │
│  │   /upload  │  │   /chat     │  │   /tickets          │  │
│  │  Endpoint  │  │  Endpoint   │  │   Endpoint          │  │
│  └────────────┘  └─────────────┘  └─────────────────────┘  │
└──────────────────────────────────────────────────────────────┘
         ↓                    ↓                    ↓
     ┌───────┐          ┌──────────┐        ┌──────────┐
     │  PDF/ │          │ ChromaDB │        │ SQLite   │
     │  TXT  │          │ Vector   │        │Database  │
     │ Files │          │Database  │        │Tickets   │
     └───────┘          └──────────┘        └──────────┘
                              ↓
                        ┌──────────────┐
                        │  OpenAI API  │
                        │  (GPT-3.5)   │
                        └──────────────┘
```

## Component Architecture

### Frontend (React + Vite)

```
src/
├── App.jsx                 # Main app component, page routing
├── main.jsx               # Entry point
├── api.js                 # API communication layer
│
├── components/
│   ├── Navigation.jsx     # Top navigation bar
│   ├── ChatBox.jsx        # Message input component
│   ├── MessageBubble.jsx  # Individual message display
│   └── UploadDocument.jsx # File upload interface
│
├── pages/
│   ├── ChatPage.jsx       # Main chat interface
│   ├── AdminPage.jsx      # Admin document management
│   └── TicketsPage.jsx    # Support tickets view
│
└── styles/
    ├── App.css            # Global styles
    ├── ChatPage.css       # Chat page styles
    ├── AdminPage.css      # Admin page styles
    └── TicketsPage.css    # Tickets page styles
```

**Key Features**:
- Component-based architecture
- State management with React hooks
- Axios for API communication
- CSS with CSS variables for theming
- Responsive design with media queries

### Backend (FastAPI + ChromaDB + SQLite)

```
backend/
├── main.py        # Main FastAPI application
├── database.py    # SQLite database management
├── utils.py       # Text processing utilities
├── requirements.txt
└── .env          # Environment variables (API keys)
```

**Key Features**:
- REST API endpoints
- CORS enabled for frontend
- Vector database integration
- File upload handling
- Database ORM

## Data Flow

### 1. Document Upload Flow

```
User uploads PDF/TXT
         ↓
[UploadDocument Component]
         ↓
POST /upload endpoint
         ↓
Extract text (PDF or TXT)
         ↓
Split into chunks (500 chars, 100 overlap)
         ↓
Embed with OpenAI API
         ↓
Store in ChromaDB
         ↓
Return success message
         ↓
UI shows "✅ Document uploaded"
```

### 2. Chat Query Flow

```
User types question
         ↓
[ChatBox Component]
         ↓
POST /chat endpoint with question
         ↓
Search ChromaDB for top 3 relevant chunks
         ↓
Create prompt with:
  - System instructions
  - Retrieved context
  - User question
         ↓
Call OpenAI GPT-3.5
         ↓
Check if answer contains "don't have enough information"
         ↓
If yes → Create support ticket
If no → Return answer with sources
         ↓
[MessageBubble Component]
         ↓
Display answer and sources to user
```

### 3. Ticket Creation Flow

```
AI response indicates insufficient information
         ↓
INSERT INTO tickets table
         ↓
ticket_id = lastrowid
         ↓
Return response with ticket_id=123
         ↓
UI shows: "✅ Support ticket #123 created"
```

### 4. Ticket Retrieval Flow

```
User clicks "Support Tickets" page
         ↓
GET /tickets endpoint
         ↓
SELECT FROM tickets WHERE status='unresolved'
         ↓
Sort by created_date DESC
         ↓
Return JSON array of tickets
         ↓
[TicketsPage Component]
         ↓
Display cards with ticket details
```

## Database Schema

### SQLite Table: tickets

```sql
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'unresolved',
    created_date TEXT NOT NULL,
    resolved_date TEXT
)
```

**Example data**:
```
id | question                      | status     | created_date
1  | How do I reset password?       | unresolved | 2024-01-15T10:30:00
2  | What's your company address?   | unresolved | 2024-01-15T11:45:00
```

## Vector Database (ChromaDB)

### Collections Structure

```
Collection: documents
├── id: "refund-policy.txt_0"
├── document: "text chunk..."
├── metadata: {
│   "source": "refund-policy.txt",
│   "chunk_index": 0,
│   "total_chunks": 45
│ }
└── embedding: [0.123, 0.456, ...] (auto-generated)
```

**Search Process**:
1. Question → OpenAI embedding
2. Query ChromaDB with embedding
3. Return top 3 most similar chunks
4. Include metadata (source document)

## API Endpoints

### 1. Upload Document
```
POST /upload
Content-Type: multipart/form-data

Request:
- file: PDF or TXT file

Response:
{
  "message": "Document uploaded successfully",
  "file_name": "pricing-faq.txt",
  "chunks_added": 45
}
```

### 2. Chat
```
POST /chat
Content-Type: application/json

Request:
{
  "question": "What's your refund policy?"
}

Response:
{
  "answer": "We offer a 30-day money-back guarantee...",
  "sources": ["refund-policy.txt"],
  "ticket_created": false,
  "ticket_id": null
}
```

### 3. Get Tickets
```
GET /tickets

Response:
[
  {
    "id": 1,
    "question": "How do I cancel my subscription?",
    "status": "unresolved",
    "created_date": "2024-01-15T10:30:00"
  }
]
```

## Text Processing Pipeline

### Document Chunking Strategy

```
Original Text: "Large document with thousands of characters..."

Step 1: Define parameters
- chunk_size = 500 characters
- overlap = 100 characters

Step 2: Create overlapping chunks
Chunk 1: chars 0-500
Chunk 2: chars 400-900    (100 char overlap)
Chunk 3: chars 800-1300   (100 char overlap)
...

Benefits:
- Preserves context between chunks
- Handles boundary cases
- Better retrieval accuracy
```

### Text Extraction

**PDF Files**:
```python
PyPDF2.PdfReader(file)
→ Extract text from each page
→ Concatenate with newlines
```

**TXT Files**:
```python
file.decode('utf-8')
→ Handle encoding errors gracefully
→ Fallback to 'latin-1' if needed
```

## RAG (Retrieval-Augmented Generation) System

### How RAG Works

```
Question: "What's your refund policy?"

1. RETRIEVAL PHASE
   └─ Find relevant documents in vector DB
     └─ Top 3 chunks about refunds

2. AUGMENTATION PHASE
   └─ Combine retrieved context with question:
     ├─ System prompt
     ├─ Retrieved documents
     └─ User question

3. GENERATION PHASE
   └─ Send augmented prompt to GPT-3.5
     └─ Get context-aware answer

Result: Accurate, cited answer from your documents
```

### System Prompt

```
"You are a customer support AI assistant. 
Answer only using the provided company document context.
If the answer is not clearly available in the context, 
say: 'I don't have enough information to answer this. 
I will create a support ticket for our team.'
Do not make up answers. Be concise and helpful."
```

## Security Considerations

### Frontend Security
- ✅ CORS enabled only for localhost
- ✅ No sensitive data in localStorage
- ✅ API keys never exposed to frontend

### Backend Security
- ✅ Environment variables for API keys
- ✅ File type validation (PDF/TXT only)
- ✅ Input validation with Pydantic
- ✅ SQLite prevents SQL injection
- ✅ CORS configured properly

### API Key Management
- ✅ Store in .env file
- ✅ Load with python-dotenv
- ✅ Never commit to git (.gitignore)
- ✅ Example file (.env.example) in repo

## Performance Considerations

### Search Performance
- Vector search: <100ms
- Top 3 retrieval: O(1) with embeddings
- Database queries: <50ms

### API Performance
- GPT response time: 1-3 seconds (varies)
- File upload: depends on file size
- Embedding generation: <500ms per document

### Optimization Tips
1. **Chunk Size**: 500 chars works well
2. **Overlap**: 100 chars prevents context loss
3. **Search Results**: Top 3 is optimal
4. **Caching**: Consider caching common questions
5. **Indexing**: ChromaDB handles automatically

## Deployment Considerations

### Frontend Deployment
- Build: `npm run build`
- Output: `dist/` folder
- Platforms: Vercel, Netlify, GitHub Pages
- Update API URL before deployment

### Backend Deployment
- Framework: FastAPI with Uvicorn
- Platforms: Heroku, AWS, Google Cloud, Vercel
- Database: SQLite or cloud PostgreSQL
- Vector DB: ChromaDB (can use persistent mode)

### Environment Variables
```bash
# Production
OPENAI_API_KEY=sk-...
DATABASE_URL=postgresql://...
FRONTEND_URL=https://yourdomain.com
```

## Scalability Challenges

### Current Limitations
- SQLite not suitable for production
- ChromaDB on disk limited
- No user authentication
- No rate limiting

### Production Improvements
1. **Database**: PostgreSQL instead of SQLite
2. **Vector DB**: Pinecone or Weaviate
3. **Auth**: JWT tokens, user management
4. **Caching**: Redis for query caching
5. **Queue**: Celery for async uploads
6. **Monitoring**: Logging and analytics

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Frontend | React 18 | UI framework |
| Frontend Build | Vite | Fast build tool |
| Frontend HTTP | Axios | API calls |
| Backend | FastAPI | Web framework |
| Backend Server | Uvicorn | ASGI server |
| AI | OpenAI API | LLM |
| Vector DB | ChromaDB | Semantic search |
| Database | SQLite | Ticket storage |
| Env | python-dotenv | Config management |
| File Upload | python-multipart | Multipart handling |
| PDF | PyPDF2 | PDF extraction |

## Development Workflow

### Local Development
```
Terminal 1: Backend
cd backend
source venv/bin/activate
python main.py

Terminal 2: Frontend
cd frontend
npm run dev

Terminal 3: Testing/Debugging
Browser DevTools
ChromaDB persistence folder
SQLite database file
```

### Testing the Flow
1. Upload document via UI
2. Check ChromaDB folder for data
3. Check SQLite db for tickets
4. Check API response timing
5. Monitor browser console

## Future Enhancements

1. **Conversation Memory**: Store chat history
2. **Multi-turn Dialog**: Context awareness
3. **Document Management**: Version control
4. **Analytics**: Question tracking
5. **A/B Testing**: Prompt variations
6. **Voice Support**: Whisper API
7. **Multi-language**: Translation support
8. **Admin Dashboard**: Team management

---

For more details, see `README.md` and inline code comments.
