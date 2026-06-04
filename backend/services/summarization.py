"""
Conversation summarization and agent-assist suggestions via OpenAI.
"""
import os
from openai import OpenAI


def get_openai_client():
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def summarize_conversation(messages: list) -> str:
    """Summarize a conversation into 2-3 sentences for the ticket description."""
    if not messages:
        return "No messages to summarize."

    conversation_text = "\n".join(
        f"{m['sender'].upper()}: {m['content']}" for m in messages
    )

    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Summarize this customer support conversation in 2-3 sentences. Focus on the main issue and whether it was resolved."},
                {"role": "user", "content": conversation_text},
            ],
            max_tokens=150,
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Summary unavailable: {e}"


def get_agent_suggestion(question: str, conversation_history: list) -> dict:
    """Return a suggested reply and troubleshooting steps for a human agent."""
    history_text = "\n".join(
        f"{m['sender'].upper()}: {m['content']}" for m in conversation_history[-6:]
    )

    try:
        client = get_openai_client()
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an expert customer support assistant helping a human agent. "
                        "Based on the conversation, provide:\n"
                        "1. A suggested reply the agent can send\n"
                        "2. Troubleshooting steps the agent should follow\n"
                        "Be concise and practical."
                    ),
                },
                {
                    "role": "user",
                    "content": f"Conversation so far:\n{history_text}\n\nCurrent issue: {question}",
                },
            ],
            max_tokens=400,
        )
        return {"suggestion": response.choices[0].message.content}
    except Exception as e:
        return {"suggestion": f"Suggestion unavailable: {e}"}
