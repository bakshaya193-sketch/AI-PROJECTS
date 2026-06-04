# 📚 Complete File Reference Guide

A complete guide to every file in the AI Customer Support Agent project.

---

## 📖 Documentation Files (Start Here!)

### README.md (Primary Setup Guide)
- **Size**: 8000+ words
- **Purpose**: Complete setup and usage guide
- **Read First**: Yes! Start here for full understanding
- **Covers**: Installation, API reference, troubleshooting, features
- **Time**: 20-30 minutes

### QUICKSTART.md (Fast Setup)
- **Size**: 500 words
- **Purpose**: Get running in 5 minutes
- **Read First**: If you're in a hurry
- **Covers**: Minimal setup, quick testing
- **Time**: 5 minutes

### ARCHITECTURE.md (System Design)
- **Size**: 5000+ words
- **Purpose**: Deep dive into how the system works
- **Read After**: Understanding basic setup
- **Covers**: Data flow, RAG pipeline, database schema, scalability
- **Time**: 30-40 minutes

### VERIFICATION.md (Testing Checklist)
- **Size**: 2000 words
- **Purpose**: Verify your setup is correct
- **Read When**: After completing setup
- **Covers**: Step-by-step verification, troubleshooting
- **Time**: 20-30 minutes

### PROJECT_SUMMARY.md (Overview)
- **Size**: 2000 words
- **Purpose**: High-level project overview
- **Read When**: Want quick summary
- **Covers**: What's included, features, tech stack, portfolio value
- **Time**: 10 minutes

### FILE_REFERENCE.md (This File)
- **Size**: 2000+ words
- **Purpose**: Guide to every file in the project
- **Read When**: Need to understand file structure
- **Covers**: Every file, its purpose, and location
- **Time**: 15-20 minutes

### .gitignore
- **Size**: 30 lines
- **Purpose**: Tell git what to ignore
- **Important**: Keep this! Don't commit .env or node_modules
- **Contains**: Patterns for backend, frontend, IDEs, OS files

---

## 🔧 Backend Files

### main.py (FastAPI Application)
**Location**: `backend/main.py`
**Size**: 305 lines
**Purpose**: Core backend application with all API endpoints

**Key Sections**:
- Lines 1-40: Imports and FastAPI setup
- Lines 41-52: ChromaDB initialization
- Lines 59-81: Pydantic models (request/response)
- Lines 84-100: Root and health endpoints
- Lines 103-167: Upload endpoint (POST /upload)
- Lines 170-263: Chat endpoint (POST /chat)
- Lines 266-299: Tickets endpoint (GET /tickets)

**Key Endpoints**:
- `GET /` - API info
- `GET /health` - Health check
- `POST /upload` - Upload documents
- `POST /chat` - Chat with AI
- `GET /tickets` - Get support tickets

**Important Config**:
- Line 26: CORS allow_origins for frontend
- Line 36: OpenAI API key loading
- Line 207: System prompt for AI

### database.py (SQLite Management)
**Location**: `backend/database.py`
**Size**: 85 lines
**Purpose**: Database initialization and connection management

**Key Functions**:
- `get_db_connection()` - Create DB connection
- `init_db()` - Create tables (called on startup)
- `create_ticket()` - Insert new ticket
- `get_all_tickets()` - Fetch unresolved tickets

**Database File**: `backend/support_tickets.db` (created on first run)

**Table Schema**:
```sql
CREATE TABLE tickets (
    id INTEGER PRIMARY KEY,
    question TEXT NOT NULL,
    status TEXT DEFAULT 'unresolved',
    created_date TEXT NOT NULL,
    resolved_date TEXT
)
```

### utils.py (Text Processing)
**Location**: `backend/utils.py`
**Size**: 85 lines
**Purpose**: Utility functions for document processing

**Key Functions**:
- `extract_text_from_pdf(content)` - Extract PDF text using PyPDF2
- `extract_text_from_txt(content)` - Extract TXT text
- `chunk_text(text, chunk_size, overlap)` - Split text into chunks

**Important Parameters**:
- `chunk_size`: 500 characters (adjustable)
- `overlap`: 100 characters between chunks

### requirements.txt (Python Dependencies)
**Location**: `backend/requirements.txt`
**Size**: 8 lines
**Purpose**: List all Python packages needed

**Packages**:
- fastapi==0.104.1 - Web framework
- uvicorn==0.24.0 - ASGI server
- python-dotenv==1.0.0 - Environment variables
- openai==0.27.8 - OpenAI API client
- chromadb==0.3.21 - Vector database
- PyPDF2==3.0.1 - PDF processing
- pydantic==2.5.0 - Data validation
- python-multipart==0.0.6 - File uploads

### .env.example (Environment Template)
**Location**: `backend/.env.example`
**Size**: 2 lines
**Purpose**: Template for environment variables

**What to Do**:
1. Copy to `.env`: `cp .env.example .env`
2. Edit `.env` and add your OpenAI API key
3. Never commit `.env` to git

**Content**:
```
OPENAI_API_KEY=sk-your-api-key-here
```

### .env (Environment Variables) ⚠️
**Location**: `backend/.env`
**Purpose**: Your actual API keys and secrets
**Important**: 
- ⚠️ Don't commit to git!
- ⚠️ Don't share with anyone!
- ⚠️ Keep it safe!

---

## ⚛️ Frontend Files

### package.json (NPM Dependencies)
**Location**: `frontend/package.json`
**Size**: 25 lines
**Purpose**: NPM package configuration

**Scripts**:
- `npm run dev` - Start development server (port 5173)
- `npm run build` - Build for production
- `npm run preview` - Preview production build

**Dependencies**:
- react@18.2.0 - UI library
- react-dom@18.2.0 - DOM rendering
- axios@1.6.0 - HTTP client

### vite.config.js (Build Configuration)
**Location**: `frontend/vite.config.js`
**Size**: 10 lines
**Purpose**: Configure Vite development and build

**Config**:
- React plugin enabled
- Dev server on localhost:5173
- ES modules enabled

### index.html (HTML Entry Point)
**Location**: `frontend/index.html`
**Size**: 14 lines
**Purpose**: HTML template for React app

**Important**:
- Root div with id="root" for React
- Script src="/src/main.jsx" for entry point
- Meta tags for viewport and charset

### src/main.jsx (React Entry Point)
**Location**: `frontend/src/main.jsx`
**Size**: 10 lines
**Purpose**: Create React root and render App

**Does**:
1. Import React and ReactDOM
2. Import App component and global CSS
3. Render App into root element

### src/App.jsx (Main App Component)
**Location**: `frontend/src/App.jsx`
**Size**: 60 lines
**Purpose**: Main app component with routing and navigation

**Features**:
- Routes between pages (Chat, Admin, Tickets)
- Backend connection check (health check)
- Navigation bar rendering
- Page selection state

**Pages**:
- currentPage === 'chat' → ChatPage
- currentPage === 'admin' → AdminPage
- currentPage === 'tickets' → TicketsPage

### src/api.js (API Service Layer)
**Location**: `frontend/src/api.js`
**Size**: 55 lines
**Purpose**: Centralized API communication

**Functions**:
- `sendChatMessage(question)` - POST /chat
- `uploadDocument(file)` - POST /upload
- `getTickets()` - GET /tickets
- `healthCheck()` - GET /health

**API Base URL**: `http://localhost:8000`

---

## 🎨 Components (Reusable React Components)

### Navigation.jsx
**Location**: `frontend/src/components/Navigation.jsx`
**Purpose**: Top navigation bar with page links
**Props**: 
- `currentPage`: Current page ID
- `setCurrentPage`: Function to change page

**Features**:
- Logo and branding
- Three nav links (Chat, Admin, Tickets)
- Active page highlighting

### ChatBox.jsx
**Location**: `frontend/src/components/ChatBox.jsx`
**Purpose**: Message input form
**Props**:
- `onSendMessage`: Callback function
- `isLoading`: Loading state

**Features**:
- Textarea input
- Send button
- Enter key to submit
- Shift+Enter for newlines
- Disabled state while loading

### MessageBubble.jsx
**Location**: `frontend/src/components/MessageBubble.jsx`
**Purpose**: Individual message display
**Props**:
- `message`: Message object with text, type, sources, etc.

**Features**:
- User vs AI styling
- Source citations
- Ticket creation notification
- Word wrapping

### UploadDocument.jsx
**Location**: `frontend/src/components/UploadDocument.jsx`
**Purpose**: File upload interface
**Features**:
- File input with drag-and-drop style
- Success/error messages
- Upload guidelines
- Loading state

---

## 📄 Pages (Full Page Components)

### ChatPage.jsx
**Location**: `frontend/src/pages/ChatPage.jsx`
**Size**: 70 lines
**Purpose**: Main chat interface

**Features**:
- Chat message history
- Auto-scroll to latest message
- ChatBox input component
- MessageBubble display
- API error handling
- Loading states

**State**:
- `messages`: Array of chat messages
- `isLoading`: Loading state during API call

### AdminPage.jsx
**Location**: `frontend/src/pages/AdminPage.jsx`
**Size**: 45 lines
**Purpose**: Admin panel for document upload

**Features**:
- UploadDocument component
- How-it-works instructions
- Step-by-step guide with cards

**Sections**:
1. Upload Documents
2. AI Training
3. Answer Questions
4. Track Tickets

### TicketsPage.jsx
**Location**: `frontend/src/pages/TicketsPage.jsx`
**Size**: 110 lines
**Purpose**: Display support tickets

**Features**:
- Fetch tickets from API
- Auto-refresh every 30 seconds
- Refresh button
- Ticket cards with details
- Empty state
- Loading state
- Error handling

**Displays**:
- Ticket ID
- Customer question
- Status (unresolved/resolved)
- Creation date

---

## 🎨 Styling Files (CSS)

### App.css (Global Styles)
**Location**: `frontend/src/styles/App.css`
**Size**: 300+ lines
**Purpose**: Global styling and layout

**Sections**:
- CSS variables (colors, shadows, transitions)
- Global element styles
- Navigation bar
- Footer
- Connection warning
- Responsive design (breakpoints at 768px, 480px)

**Color Scheme**:
- Primary: #2563eb (blue)
- Secondary: #10b981 (green)
- Danger: #ef4444 (red)
- Dark: #1f2937
- Light: #f3f4f6

### ChatPage.css
**Location**: `frontend/src/styles/ChatPage.css`
**Size**: 350+ lines
**Purpose**: Chat page specific styles

**Includes**:
- Chat container layout
- Message bubbles (user vs AI)
- Input area and button
- Source citations
- Ticket notifications
- Animations (slideIn, float, pulse)
- Mobile responsive

### AdminPage.css
**Location**: `frontend/src/styles/AdminPage.css`
**Size**: 300+ lines
**Purpose**: Admin page specific styles

**Includes**:
- Upload container layout
- Upload box styling
- File input styling
- Success/error messages
- Instructions grid
- Instruction cards
- Hover effects

### TicketsPage.css
**Location**: `frontend/src/styles/TicketsPage.css`
**Size**: 350+ lines
**Purpose**: Tickets page specific styles

**Includes**:
- Tickets header
- Refresh button
- Tickets grid layout
- Ticket cards
- Status badges
- Empty state
- Loading state
- Responsive grid

---

## 📚 Sample Documents

### refund-policy.txt
**Location**: `sample-documents/refund-policy.txt`
**Size**: 2500+ words
**Purpose**: Company refund policy

**Sections**:
- 30-Day Money-Back Guarantee
- How to Request Refund
- Refund Eligibility
- Items Not Eligible
- Process Timeline
- Partial Refunds
- Shipping Costs

### shipping-policy.txt
**Location**: `sample-documents/shipping-policy.txt`
**Size**: 2500+ words
**Purpose**: Shipping information and options

**Sections**:
- Shipping Options (Standard, Express, Overnight, International)
- Shipping Costs
- Tracking
- Delivery Address
- Holiday Shipping
- Damaged/Lost Packages
- Returns Shipping

### password-reset-guide.txt
**Location**: `sample-documents/password-reset-guide.txt`
**Size**: 2000+ words
**Purpose**: Password reset instructions

**Sections**:
- Forgot Password Process
- Password Requirements
- Reset Email
- Link Expiration
- Security Tips
- 2FA
- Account Recovery

### pricing-faq.txt
**Location**: `sample-documents/pricing-faq.txt`
**Size**: 2500+ words
**Purpose**: Pricing and FAQ

**Sections**:
- General Pricing Questions
- Billing and Payments
- Refunds and Cancellations
- Upgrade/Downgrade
- Enterprise Pricing
- Features and Limits
- Taxes
- Special Offers

---

## 🚀 Setup and Configuration Files

### setup-windows.bat
**Location**: `setup-windows.bat`
**Purpose**: Automated setup for Windows users

**Does**:
1. Check Python and Node.js installed
2. Create Python virtual environment
3. Install backend dependencies
4. Install frontend dependencies
5. Create .env file
6. Prompt for API key

**How to Use**:
```bash
Double-click setup-windows.bat
```

### setup-macos.sh
**Location**: `setup-macos.sh`
**Purpose**: Automated setup for macOS/Linux users

**Does**: Same as Windows batch file

**How to Use**:
```bash
chmod +x setup-macos.sh
./setup-macos.sh
```

---

## 📋 Summary Statistics

| Category | Count | Details |
|----------|-------|---------|
| **Backend Python Files** | 3 | main.py, database.py, utils.py |
| **Frontend React Files** | 8 | App.jsx, main.jsx, 4 components, 3 pages |
| **CSS Files** | 4 | Global + 3 page-specific |
| **Configuration Files** | 3 | package.json, vite.config.js, .gitignore |
| **Documentation Files** | 7 | README, QUICKSTART, ARCHITECTURE, etc. |
| **Sample Documents** | 4 | 2500+ word content files |
| **Setup Scripts** | 2 | Windows batch, macOS shell |
| **Total Files** | 33 | Complete project |

---

## 🎯 File Organization by Purpose

### API Endpoints
- `backend/main.py` - All endpoints defined here

### Database
- `backend/database.py` - SQLite management
- `backend/support_tickets.db` - Data storage (created on first run)

### Data Processing
- `backend/utils.py` - Text extraction and chunking

### Frontend State & Logic
- `frontend/src/App.jsx` - Main app state
- `frontend/src/api.js` - API communication
- `frontend/src/pages/` - Page logic

### Frontend UI
- `frontend/src/components/` - Reusable components
- `frontend/src/styles/` - All CSS files

### Content
- `sample-documents/` - Training documents
- `frontend/index.html` - HTML structure

### Configuration
- `backend/requirements.txt` - Python deps
- `frontend/package.json` - NPM deps
- `vite.config.js` - Build config

### Documentation
- All `.md` files - Complete guides

---

## 🔍 How to Find Things

### "How do I upload files?"
→ `backend/main.py` lines 103-167 (/upload endpoint)
→ `frontend/src/components/UploadDocument.jsx`

### "How does the AI work?"
→ `backend/main.py` lines 170-263 (/chat endpoint)
→ `backend/utils.py` (text processing)

### "How are tickets stored?"
→ `backend/database.py`
→ `frontend/src/pages/TicketsPage.jsx`

### "How do I style something?"
→ `frontend/src/styles/` (find relevant CSS file)
→ Use CSS variables from `App.css`

### "How do I add a new page?"
→ Create file in `frontend/src/pages/`
→ Create CSS file in `frontend/src/styles/`
→ Import in `frontend/src/App.jsx`
→ Add route in App.jsx

### "How do I create a new API endpoint?"
→ Add function in `backend/main.py`
→ Add response model (Pydantic)
→ Add to `frontend/src/api.js`

### "Where are my API keys?"
→ `backend/.env` (don't commit!)
→ `.env.example` (template)

---

## ✅ File Checklist

Before running the project, verify:
- [ ] All backend files exist (main.py, database.py, utils.py)
- [ ] All frontend files exist (React components, pages, styles)
- [ ] All sample documents exist (4 files)
- [ ] `.env` created with API key
- [ ] `requirements.txt` can be read
- [ ] `package.json` can be read
- [ ] `.gitignore` exists

---

## 🎓 Recommended Reading Order

1. **START**: This file (FILE_REFERENCE.md) - 15 min
2. **QUICKSTART.md** - 5 min
3. **Setup your system** - 10 min
4. **README.md** - 20 min (learn features)
5. **VERIFICATION.md** - Test everything
6. **ARCHITECTURE.md** - Deep dive (30 min)
7. **Code files** - Explore and customize

---

This file reference should help you navigate the entire project structure!
