"""
Chat endpoint with:
- Language detection & translation
- Sentiment analysis
- RAG via ChromaDB
- Auto-ticket creation
- Human escalation logic
- Background notifications
"""
import os
import re
import uuid
from datetime import datetime
from typing import Optional
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from openai import OpenAI
from database import get_db_connection
from chroma_store import get_collection
from services.translation import detect_language, translate_to_english, translate_from_english
from services.sentiment import analyze_sentiment
from services.notifications import notify_new_ticket

router = APIRouter()

# Lazy-initialized so .env is loaded first
_openai_client = None

def get_openai():
    global _openai_client
    if _openai_client is None:
        # timeout + retries make the connection more resilient in cloud containers
        # .strip() removes any trailing newline/spaces that would make the
        # Authorization header invalid (a common copy-paste issue)
        _openai_client = OpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "").strip(),
            timeout=60.0,
            max_retries=3,
        )
    return _openai_client

# Short acknowledgements / greetings that should NEVER create a ticket
SMALL_TALK = {
    "ok", "okay", "kk", "k", "thanks", "thank you", "thankyou", "ty", "thx",
    "great", "cool", "nice", "good", "got it", "alright", "all right", "fine",
    "yes", "no", "yep", "nope", "sure", "perfect", "awesome", "hmm", "oh",
    "hi", "hii", "hey", "hello", "yo", "good morning", "good evening",
    "good afternoon", "bye", "goodbye", "see you", "np", "no problem", "welcome",
}

AGENT_KEYWORDS = [
    "talk to agent", "human agent", "real person", "speak to someone",
    "connect to agent", "connect to an agent", "connect me to an agent",
    "speak to agent", "speak to an agent", "talk to human", "talk to a human",
    "need an agent", "want an agent", "get an agent", "need a human",
    "live agent", "live support", "human support", "call me",
    "transfer me", "escalate", "help from a person", "reach an agent"
]


class ChatRequest(BaseModel):
    question: str
    session_id: Optional[str] = None
    language_override: Optional[str] = None
    user_id: Optional[int] = None  # set when customer is logged in


class ChatResponse(BaseModel):
    answer: str
    sources: list
    ticket_created: bool
    ticket_id: Optional[int] = None
    session_id: str
    detected_language: str
    sentiment: str
    sentiment_score: float
    escalated: bool
    routed_to_agent: bool = False


# ── helpers ──────────────────────────────────────────────────────────────────

def _get_or_create_conversation(session_id: str, language: str, user_id: int = None) -> int:
    conn = get_db_connection()
    cur = conn.cursor()
    # If user_id given, find their existing conversation first
    if user_id:
        cur.execute("SELECT id FROM conversations WHERE user_id = ? ORDER BY created_date DESC LIMIT 1", (user_id,))
        row = cur.fetchone()
        if row:
            conv_id = row["id"]
            cur.execute("UPDATE conversations SET updated_date = ? WHERE id = ?", (datetime.now().isoformat(), conv_id))
            conn.commit()
            conn.close()
            return conv_id
    cur.execute("SELECT id FROM conversations WHERE session_id = ?", (session_id,))
    row = cur.fetchone()
    now = datetime.now().isoformat()
    if row:
        conv_id = row["id"]
        cur.execute("UPDATE conversations SET updated_date = ? WHERE id = ?", (now, conv_id))
    else:
        cur.execute(
            "INSERT INTO conversations (session_id, user_id, status, language, created_date, updated_date) VALUES (?,?,?,?,?,?)",
            (session_id, user_id, "active", language, now, now),
        )
        conv_id = cur.lastrowid
    conn.commit()
    conn.close()
    return conv_id


def _save_message(conv_id, sender, content, original, language, sentiment, score):
    conn = get_db_connection()
    conn.execute(
        "INSERT INTO messages (conversation_id, sender, content, original_content, language, sentiment, sentiment_score, created_date) VALUES (?,?,?,?,?,?,?,?)",
        (conv_id, sender, content, original, language, sentiment, score, datetime.now().isoformat()),
    )
    conn.commit()
    conn.close()


def _needs_escalation(conv_id: int) -> bool:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as c FROM messages WHERE conversation_id=? AND sender='bot' AND content LIKE '%support ticket%'", (conv_id,))
    fallbacks = cur.fetchone()["c"]
    cur.execute("SELECT COUNT(*) as c FROM messages WHERE conversation_id=? AND sentiment='negative'", (conv_id,))
    negatives = cur.fetchone()["c"]
    conn.close()
    return fallbacks >= 2 or negatives >= 3


def _get_config(key: str) -> str:
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT value FROM config WHERE key = ?", (key,))
    row = cur.fetchone()
    conn.close()
    return row["value"] if row else ""


# ── endpoint ─────────────────────────────────────────────────────────────────

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest, background_tasks: BackgroundTasks):
    question = request.question.strip()
    if not question:
        raise HTTPException(status_code=400, detail="Question cannot be empty")

    session_id = request.session_id or str(uuid.uuid4())

    # 1. Detect language (or use manual override)
    detected_lang = request.language_override or detect_language(question)

    # 2. Translate question to English for embeddings
    english_question = translate_to_english(question, detected_lang)

    # 3. Sentiment analysis
    s = analyze_sentiment(question)
    sentiment, score = s["sentiment"], s["score"]

    # force_escalate ONLY when user explicitly asks for a human agent
    q_lower = question.lower()
    force_escalate = any(kw in q_lower for kw in AGENT_KEYWORDS)

    # Also catch phrases with "agent" OR "human" combined with connection intent words
    connection_words = ["connect", "speak", "talk", "reach", "need", "want", "get", "transfer"]
    human_words = ["agent", "human", "person", "someone", "representative", "staff", "support"]
    if not force_escalate:
        has_connection = any(w in q_lower for w in connection_words)
        has_human = any(w in q_lower for w in human_words)
        force_escalate = has_connection and has_human

    # 4. Persist conversation + user message
    conv_id = _get_or_create_conversation(session_id, detected_lang, request.user_id)

    # Update customer last active timestamp
    conn = get_db_connection()
    conn.execute("UPDATE conversations SET customer_last_active=? WHERE id=?", (datetime.now().isoformat(), conv_id))
    conn.commit()
    conn.close()

    # Check if agent is active — if so, save message and return without AI
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT agent_active, agent_name FROM conversations WHERE id=?", (conv_id,))
    conv_row = cur.fetchone()
    conn.close()

    if conv_row and conv_row["agent_active"]:
        _save_message(conv_id, "user", question, english_question, detected_lang, sentiment, score)
        return ChatResponse(
            answer="",
            sources=[],
            ticket_created=False,
            ticket_id=None,
            session_id=session_id,
            detected_language=detected_lang,
            sentiment=sentiment,
            sentiment_score=score,
            escalated=False,
            routed_to_agent=True,
        )
    _save_message(conv_id, "user", question, english_question, detected_lang, sentiment, score)

    # 4b. Small talk / acknowledgements — reply naturally, NEVER create a ticket.
    # Strip emojis & punctuation, keep only letters/spaces, then compare.
    cleaned = re.sub(r"[^a-z\s]", "", english_question.lower()).strip()
    cleaned = re.sub(r"\s+", " ", cleaned)
    if cleaned in SMALL_TALK or len(cleaned.replace(" ", "")) <= 2:
        if any(g in cleaned.split() for g in ["hi", "hii", "hey", "hello", "yo", "morning", "evening", "afternoon"]):
            reply_en = "Hello! How can I help you today?"
        elif any(t in cleaned for t in ["thank", "thx", "ty"]):
            reply_en = "You're welcome! Is there anything else I can help you with? 😊"
        elif any(b in cleaned for b in ["bye", "goodbye", "see you"]):
            reply_en = "Goodbye! Have a great day. 😊"
        else:
            reply_en = "Great! Let me know if you have any other questions. 😊"
        reply = translate_from_english(reply_en, detected_lang)
        _save_message(conv_id, "bot", reply, reply_en, detected_lang, "neutral", 0.0)
        return ChatResponse(
            answer=reply, sources=[], ticket_created=False, ticket_id=None,
            session_id=session_id, detected_language=detected_lang,
            sentiment=sentiment, sentiment_score=score, escalated=False,
        )

    # 5. RAG: search ChromaDB
    try:
        results = get_collection().query(query_texts=[english_question], n_results=3, include=["documents", "metadatas"])
    except Exception:
        results = {"documents": [[]], "metadatas": [[]]}

    context, sources = "", []
    if results["documents"] and results["documents"][0]:
        for doc, meta in zip(results["documents"][0], results["metadatas"][0]):
            context += f"\n{doc}"
            src = meta.get("source", "Unknown")
            if src not in sources:
                sources.append(src)

    # 6. Build prompt with sentiment tone adjustment
    tone = "The customer seems frustrated or upset. Start with a sincere apology and be extra empathetic. " if sentiment == "negative" else ""

    # If user wants to connect to an agent, give a friendly response
    agent_request = force_escalate

    if agent_request:
        system_prompt = (
            "You are a customer support AI assistant. "
            "The customer wants to speak to a human agent. "
            "Respond warmly and let them know you are connecting them to a support agent. "
            "Say something like: 'Of course! I'm connecting you to one of our support agents right away. "
            "Please hold on, someone will be with you shortly.' "
            "Keep it friendly and reassuring. Do not mention tickets."
        )
    else:
        system_prompt = (
            f"You are a customer support AI assistant. {tone}"
            "Use the provided company document context to help the customer as much as possible. "
            "If the context contains information relevant to the question, ANSWER it helpfully — "
            "even when the question is phrased personally (e.g. 'will I get a refund?', 'can I return this?'), "
            "explain the relevant policy, the eligibility conditions, and the steps from the documents. "
            "Do not refuse just because you don't know the customer's specific order details; instead, "
            "explain what the policy says and what conditions apply. "
            "For greetings or small talk (like 'hi', 'thanks', 'ok'), reply naturally without creating a ticket. "
            "ONLY reply with exactly: 'I don't have enough information to answer this. I will create a support ticket for our team.' "
            "if the documents contain nothing relevant to the question at all. "
            "Never invent facts that are not in the context. Be concise, friendly, and helpful."
        )

    try:
        ai_response = get_openai().chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Context:\n{context or 'No documents uploaded yet.'}\n\nQuestion: {english_question}"},
            ],
            temperature=0.7,
            max_tokens=500,
        )
        answer_en = ai_response.choices[0].message.content
    except Exception as e:
        # Surface the real OpenAI error instead of a generic 500
        err_type = type(e).__name__
        err_msg = str(e)
        # Note: do NOT log the underlying cause — it can contain the API key
        print(f"[OpenAI error] {err_type}: {err_msg}")
        if "quota" in err_msg.lower() or "insufficient" in err_msg.lower():
            friendly = "⚠️ The AI service is temporarily unavailable (API quota exceeded). Please contact the administrator."
        elif "api_key" in err_msg.lower() or "authentication" in err_msg.lower() or "401" in err_msg:
            friendly = "⚠️ The AI service is not configured correctly (API key issue). Please contact the administrator."
        else:
            friendly = f"⚠️ AI service error: {err_type}. Please try again later."
        answer = translate_from_english(friendly, detected_lang)
        _save_message(conv_id, "bot", answer, friendly, detected_lang, "neutral", 0.0)
        return ChatResponse(
            answer=answer, sources=[], ticket_created=False, ticket_id=None,
            session_id=session_id, detected_language=detected_lang,
            sentiment=sentiment, sentiment_score=score, escalated=False,
        )

    # 7. Translate answer back to user's language
    answer = translate_from_english(answer_en, detected_lang)

    # 8. Save bot message
    _save_message(conv_id, "bot", answer, answer_en, detected_lang, "neutral", 0.0)

    # 9. Create ticket ONLY when AI explicitly says it cannot answer
    ticket_created, ticket_id = False, None
    needs_ticket = "i don't have enough information to answer this" in answer_en.lower()

    if needs_ticket:
        priority = "high" if sentiment == "negative" else "normal"
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO tickets (conversation_id, question, status, priority, created_date) VALUES (?,?,?,?,?)",
            (conv_id, question, "unresolved", priority, datetime.now().isoformat()),
        )
        conn.commit()
        ticket_id = cur.lastrowid
        conn.close()
        ticket_created = True

        notif_email = _get_config("notification_email")
        slack_wh = _get_config("slack_webhook")
        background_tasks.add_task(notify_new_ticket, ticket_id, question, priority, notif_email, slack_wh)

    # 10. Escalation — mark conversation as escalated but only create a ticket
    # if the user explicitly requested a human agent (force_escalate)
    escalated = False
    if force_escalate:
        conn = get_db_connection()
        conn.execute("UPDATE conversations SET status='escalated' WHERE id=?", (conv_id,))
        conn.commit()
        conn.close()
        escalated = True
        if not ticket_created:
            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO tickets (conversation_id, question, status, priority, created_date) VALUES (?,?,'pending_agent','high',?)",
                (conv_id, question, datetime.now().isoformat()),
            )
            conn.commit()
            ticket_id = cur.lastrowid
            conn.close()
            ticket_created = True

    return ChatResponse(
        answer=answer, sources=sources, ticket_created=ticket_created,
        ticket_id=ticket_id, session_id=session_id, detected_language=detected_lang,
        sentiment=sentiment, sentiment_score=score, escalated=escalated,
    )


@router.get("/conversations/{session_id}/status")
def get_conversation_status(session_id: str):
    """Check if an agent is currently active in this conversation."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT agent_active, agent_name, customer_last_active FROM conversations WHERE session_id=?", (session_id,))
    row = cur.fetchone()
    conn.close()
    if not row:
        return {"agent_active": False, "agent_name": None}

    # Auto-leave if customer inactive for 5 minutes
    if row["agent_active"] and row["customer_last_active"]:
        from datetime import datetime as dt
        try:
            last = dt.fromisoformat(row["customer_last_active"])
            mins_idle = (dt.now() - last).total_seconds() / 60
            if mins_idle >= 5:
                # Auto-leave
                conn2 = get_db_connection()
                conn2.execute("UPDATE conversations SET agent_active=0, agent_name=NULL WHERE session_id=?", (session_id,))
                conn2.execute("""INSERT INTO messages (conversation_id, sender, content, original_content, language, sentiment, sentiment_score, created_date)
                    SELECT id, 'system', 'Agent has left the chat. You are now connected to AI assistant.', '', 'en', 'neutral', 0.0, ? FROM conversations WHERE session_id=?""",
                    (dt.now().isoformat(), session_id))
                conn2.commit()
                conn2.close()
                return {"agent_active": False, "agent_name": None, "auto_left": True}
        except Exception:
            pass

    return {"agent_active": bool(row["agent_active"]), "agent_name": row["agent_name"]}


@router.post("/conversations/{session_id}/agent/join")
def agent_join(session_id: str):
    """Agent joins the chat — messages will now route to agent, not AI."""
    from routes.auth import get_current_user
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM conversations WHERE session_id=?", (session_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    now = datetime.now().isoformat()
    conn.execute("UPDATE conversations SET agent_active=1, agent_joined_at=?, updated_date=? WHERE session_id=?",
                 (now, now, session_id))
    conn.execute("""INSERT INTO messages (conversation_id, sender, content, original_content, language, sentiment, sentiment_score, created_date)
        VALUES (?, 'system', 'A support agent has joined the chat.', '', 'en', 'neutral', 0.0, ?)""",
        (row["id"], now))
    conn.commit()
    conn.close()
    return {"message": "Agent joined successfully"}


@router.post("/conversations/{session_id}/agent/join-named")
def agent_join_named(session_id: str, agent_name: str = "Support Agent"):
    """Agent joins with their name displayed in chat."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM conversations WHERE session_id=?", (session_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    now = datetime.now().isoformat()
    conn.execute("UPDATE conversations SET agent_active=1, agent_name=?, agent_joined_at=?, updated_date=? WHERE session_id=?",
                 (agent_name, now, now, session_id))
    conn.execute("""INSERT INTO messages (conversation_id, sender, content, original_content, language, sentiment, sentiment_score, created_date)
        VALUES (?, 'system', ?, '', 'en', 'neutral', 0.0, ?)""",
        (row["id"], f"{agent_name} has joined the chat.", now))
    conn.commit()
    conn.close()
    return {"message": f"{agent_name} joined"}


@router.post("/conversations/{session_id}/agent/leave")
def agent_leave(session_id: str):
    """Agent leaves the chat — messages route back to AI."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM conversations WHERE session_id=?", (session_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="Conversation not found")
    now = datetime.now().isoformat()
    conn.execute("UPDATE conversations SET agent_active=0, agent_name=NULL, updated_date=? WHERE session_id=?", (now, session_id))
    conn.execute("""INSERT INTO messages (conversation_id, sender, content, original_content, language, sentiment, sentiment_score, created_date)
        VALUES (?, 'system', 'Agent has left the chat. You are now connected to AI assistant.', '', 'en', 'neutral', 0.0, ?)""",
        (row["id"], now))
    conn.commit()
    conn.close()
    return {"message": "Agent left successfully"}


@router.get("/conversations/user/{user_id}/messages")
def get_messages_by_user(user_id: int):
    """Return all messages for a customer's conversation by user_id."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id, session_id FROM conversations WHERE user_id = ? ORDER BY created_date DESC LIMIT 1", (user_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return {"session_id": None, "messages": []}
    cur.execute(
        "SELECT sender, content, language, sentiment, sentiment_score, created_date FROM messages WHERE conversation_id=? ORDER BY created_date ASC",
        (row["id"],),
    )
    msgs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return {"session_id": row["session_id"], "messages": msgs}

@router.get("/conversations/{session_id}/messages")
def get_messages(session_id: str):
    """Return all messages for a given session."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT id FROM conversations WHERE session_id = ?", (session_id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return []
    cur.execute(
        "SELECT sender, content, language, sentiment, sentiment_score, created_date FROM messages WHERE conversation_id=? ORDER BY created_date ASC",
        (row["id"],),
    )
    msgs = [dict(r) for r in cur.fetchall()]
    conn.close()
    return msgs
