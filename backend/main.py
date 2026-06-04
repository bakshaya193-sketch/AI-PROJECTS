"""
AI Customer Support Agent v2 - Main FastAPI Application
"""
import os
from dotenv import load_dotenv

# Load .env FIRST before importing any routes
load_dotenv()

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import init_db
from routes import auth, chat, upload, tickets, analytics, agent, config_route

app = FastAPI(
    title="AI Customer Support Agent v2",
    description="Full-featured AI customer support with RAG, sentiment, multilingual support",
    version="2.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(chat.router, tags=["Chat"])
app.include_router(upload.router, tags=["Upload"])
app.include_router(tickets.router, tags=["Tickets"])
app.include_router(analytics.router, tags=["Analytics"])
app.include_router(agent.router, tags=["Agent"])
app.include_router(config_route.router, tags=["Config"])

init_db()


@app.get("/")
def root():
    return {"message": "AI Customer Support Agent v2", "docs": "/docs"}


@app.get("/health")
def health():
    return {"status": "healthy", "version": "2.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
