"""
Agent-assist endpoints:
- GET /agent/tickets  - escalated/pending tickets
- GET /agent/tickets/{id}/suggest  - AI suggested reply
- POST /agent/tickets/{id}/reply  - agent sends a reply
- POST /agent/tickets/{id}/summarize  - summarize the conversation
"""
from datetime import datetime
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import get_db_connection
from routes.auth import get_current_user
from services.summarization import get_agent_suggestion, summarize_conversation

router = APIRouter()


class AgentReply(BaseModel):
    message: str


@router.get("/agent/tickets")
def get_escalated_tickets(current_user: dict = Depends(get_current_user)):
    """Return all escalated or pending-agent tickets."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        SELECT t.*, c.session_id, c.language, c.status as conv_status
        FROM tickets t
        LEFT JOIN conversations c ON t.conversation_id = c.id
        WHERE t.status IN ('pending_agent', 'unresolved')
        ORDER BY t.created_date DESC
    """)
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


@router.get("/agent/tickets/{ticket_id}/suggest")
def suggest_reply(ticket_id: int, current_user: dict = Depends(get_current_user)):
    """Return an AI-generated suggested reply and troubleshooting steps."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cur.fetchone()
    if not ticket:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    history = []
    if ticket["conversation_id"]:
        cur.execute(
            "SELECT sender, content FROM messages WHERE conversation_id = ? ORDER BY created_date ASC",
            (ticket["conversation_id"],),
        )
        history = [dict(r) for r in cur.fetchall()]

    conn.close()
    return get_agent_suggestion(ticket["question"], history)


@router.post("/agent/tickets/{ticket_id}/reply")
def agent_reply(ticket_id: int, reply: AgentReply, current_user: dict = Depends(get_current_user)):
    """Agent sends a message into the conversation."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT conversation_id FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cur.fetchone()
    if not ticket:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    if ticket["conversation_id"]:
        conn.execute(
            "INSERT INTO messages (conversation_id, sender, content, original_content, language, sentiment, sentiment_score, created_date) VALUES (?,?,?,?,?,?,?,?)",
            (ticket["conversation_id"], "agent", reply.message, reply.message, "en", "neutral", 0.0, datetime.now().isoformat()),
        )
        conn.commit()

    conn.close()
    return {"message": "Reply sent successfully"}


@router.post("/agent/tickets/{ticket_id}/summarize")
def summarize_ticket(ticket_id: int, current_user: dict = Depends(get_current_user)):
    """Generate and save an AI summary of the conversation for this ticket."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cur.fetchone()
    if not ticket:
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    history = []
    if ticket["conversation_id"]:
        cur.execute(
            "SELECT sender, content FROM messages WHERE conversation_id = ? ORDER BY created_date ASC",
            (ticket["conversation_id"],),
        )
        history = [dict(r) for r in cur.fetchall()]

    summary = summarize_conversation(history)
    conn.execute("UPDATE tickets SET summary = ? WHERE id = ?", (summary, ticket_id))
    conn.commit()
    conn.close()
    return {"summary": summary}
