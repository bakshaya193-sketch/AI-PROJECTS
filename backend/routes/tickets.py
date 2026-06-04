"""
Tickets endpoints: list, update status, get conversation for a ticket.
"""
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from database import get_db_connection
from routes.auth import get_current_user

router = APIRouter()


class Ticket(BaseModel):
    id: int
    question: str
    summary: Optional[str] = None
    status: str
    priority: str
    created_date: str
    conversation_id: Optional[int] = None


class StatusUpdate(BaseModel):
    status: str  # unresolved | pending_agent | resolved


@router.get("/tickets", response_model=list[Ticket])
def get_tickets(status: Optional[str] = None):
    """Return tickets filtered by status. Defaults to all non-resolved."""
    conn = get_db_connection()
    cur = conn.cursor()
    if status:
        cur.execute("SELECT * FROM tickets WHERE status = ? ORDER BY created_date DESC", (status,))
    else:
        cur.execute("SELECT * FROM tickets WHERE status != 'resolved' ORDER BY created_date DESC")
    rows = [dict(r) for r in cur.fetchall()]
    conn.close()
    return rows


@router.patch("/tickets/{ticket_id}")
def update_ticket(ticket_id: int, update: StatusUpdate, current_user: dict = Depends(get_current_user)):
    """Update ticket status (agents/admins only)."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM tickets WHERE id = ?", (ticket_id,))
    if not cur.fetchone():
        conn.close()
        raise HTTPException(status_code=404, detail="Ticket not found")

    resolved_date = datetime.now().isoformat() if update.status == "resolved" else None
    cur.execute(
        "UPDATE tickets SET status = ?, resolved_date = ? WHERE id = ?",
        (update.status, resolved_date, ticket_id),
    )
    conn.commit()
    conn.close()
    return {"message": f"Ticket #{ticket_id} updated to '{update.status}'"}


@router.get("/tickets/{ticket_id}/conversation-session")
def get_ticket_session(ticket_id: int, current_user: dict = Depends(get_current_user)):
    """Return the session_id for the conversation linked to a ticket."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT c.session_id FROM tickets t JOIN conversations c ON t.conversation_id = c.id WHERE t.id=?", (ticket_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        raise HTTPException(status_code=404, detail="Session not found")
    return {"session_id": row["session_id"]}


@router.get("/tickets/{ticket_id}/conversation")
def get_ticket_conversation(ticket_id: int, current_user: dict = Depends(get_current_user)):
    """Return all messages for the conversation linked to a ticket."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT conversation_id FROM tickets WHERE id = ?", (ticket_id,))
    ticket = cur.fetchone()
    if not ticket or not ticket["conversation_id"]:
        conn.close()
        return []

    cur.execute(
        "SELECT sender, content, sentiment, sentiment_score, language, created_date FROM messages WHERE conversation_id = ? ORDER BY created_date ASC",
        (ticket["conversation_id"],),
    )
    msgs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return msgs
