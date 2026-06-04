import SentimentBadge from "./SentimentBadge";

export default function MessageBubble({ message }) {
  // System notification — centered grey pill
  if (message.sender === "system") {
    return (
      <div className="system-notification">
        <span>— {message.text} —</span>
      </div>
    );
  }

  const isUser = message.type === "user" || message.sender === "user";
  const isAgent = message.sender === "agent";

  return (
    <div className={`message-container ${isUser ? "user-message" : "ai-message"}`}>
      <div className={`message-bubble ${isUser ? "user-bubble" : isAgent ? "agent-bubble" : "ai-bubble"}`}>

        {/* Sender label for non-user messages */}
        {!isUser && (
          <div className="sender-label">
            {isAgent ? "🧑‍💼 Support Agent" : "🤖 AI Assistant"}
          </div>
        )}

        <div className="message-top-row">
          <p className="message-text">{message.text}</p>
          {isUser && <SentimentBadge sentiment={message.sentiment} score={message.sentiment_score} />}
        </div>

        {/* Language indicator */}
        {message.detectedLanguage && (
          <div className="language-indicator">🌐 {message.detectedLanguage.toUpperCase()}</div>
        )}

        {/* Ticket notification */}
        {!isUser && message.ticketCreated && (
          <div className="ticket-notification">
            ✅ Support ticket #{message.ticketId} created — our team will follow up
          </div>
        )}

        {/* Escalation notice */}
        {!isUser && message.escalated && (
          <div className="escalation-notice">
            🔴 Connecting you to a human agent
          </div>
        )}
      </div>
    </div>
  );
}
