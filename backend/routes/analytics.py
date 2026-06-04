"""
Analytics endpoint - returns metrics for the dashboard.
Aggregates data from conversations, messages, and tickets tables.
"""
from fastapi import APIRouter, Depends, HTTPException
from database import get_db_connection
from routes.auth import get_current_user

router = APIRouter()


@router.get("/analytics")
def get_analytics(current_user: dict = Depends(get_current_user)):
    # Both admin and agent can view analytics
    if current_user.get("role") not in ["admin", "agent"]:
        raise HTTPException(status_code=403, detail="Access denied")
    """Return all analytics metrics."""
    conn = get_db_connection()
    cur = conn.cursor()

    # Total conversations
    cur.execute("SELECT COUNT(*) as c FROM conversations")
    total_conversations = cur.fetchone()["c"]

    # Total messages
    cur.execute("SELECT COUNT(*) as c FROM messages")
    total_messages = cur.fetchone()["c"]

    # Total tickets
    cur.execute("SELECT COUNT(*) as c FROM tickets")
    total_tickets = cur.fetchone()["c"]

    # Resolved tickets
    cur.execute("SELECT COUNT(*) as c FROM tickets WHERE status = 'resolved'")
    resolved_tickets = cur.fetchone()["c"]

    # Resolution rate
    resolution_rate = round((resolved_tickets / total_tickets * 100) if total_tickets > 0 else 0, 1)

    # Sentiment distribution
    cur.execute("""
        SELECT sentiment, COUNT(*) as count
        FROM messages WHERE sender = 'user'
        GROUP BY sentiment
    """)
    sentiment_rows = cur.fetchall()
    sentiment_distribution = {row["sentiment"]: row["count"] for row in sentiment_rows}

    # Ticket status breakdown
    cur.execute("SELECT status, COUNT(*) as count FROM tickets GROUP BY status")
    ticket_status = {row["status"]: row["count"] for row in cur.fetchall()}

    # Conversations per day (last 7 days)
    cur.execute("""
        SELECT DATE(created_date) as day, COUNT(*) as count
        FROM conversations
        WHERE created_date >= DATE('now', '-7 days')
        GROUP BY day ORDER BY day ASC
    """)
    daily_conversations = [{"day": r["day"], "count": r["count"]} for r in cur.fetchall()]

    # Top languages
    cur.execute("""
        SELECT language, COUNT(*) as count
        FROM messages WHERE sender = 'user'
        GROUP BY language ORDER BY count DESC LIMIT 5
    """)
    top_languages = [{"language": r["language"], "count": r["count"]} for r in cur.fetchall()]

    # Escalated conversations
    cur.execute("SELECT COUNT(*) as c FROM conversations WHERE status = 'escalated'")
    escalated_count = cur.fetchone()["c"]

    # Average messages per conversation
    cur.execute("""
        SELECT AVG(msg_count) as avg FROM (
            SELECT COUNT(*) as msg_count FROM messages GROUP BY conversation_id
        )
    """)
    avg_msgs = cur.fetchone()["avg"] or 0

    # Tickets by priority
    cur.execute("SELECT priority, COUNT(*) as count FROM tickets GROUP BY priority")
    tickets_by_priority = {row["priority"]: row["count"] for row in cur.fetchall()}

    conn.close()

    return {
        "total_conversations": total_conversations,
        "total_messages": total_messages,
        "total_tickets": total_tickets,
        "resolved_tickets": resolved_tickets,
        "resolution_rate": resolution_rate,
        "escalated_conversations": escalated_count,
        "avg_messages_per_conversation": round(avg_msgs, 1),
        "sentiment_distribution": sentiment_distribution,
        "ticket_status_breakdown": ticket_status,
        "tickets_by_priority": tickets_by_priority,
        "daily_conversations": daily_conversations,
        "top_languages": top_languages,
    }
