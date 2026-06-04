import { useState } from "react";

export default function ChatBox({ onSend, loading }) {
  const [text, setText] = useState("");

  const submit = (e) => {
    e.preventDefault();
    if (!text.trim()) return;
    onSend(text.trim());
    setText("");
  };

  return (
    <form className="chatbox-form" onSubmit={submit}>
      <div className="chatbox-input-container">
        <textarea
          className="chatbox-input"
          placeholder="Type your question... (Enter to send, Shift+Enter for new line)"
          value={text}
          onChange={(e) => setText(e.target.value)}
          onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); submit(e); } }}
          disabled={loading}
          rows={3}
        />
        <button type="submit" className={`chatbox-button ${loading ? "loading" : ""}`} disabled={loading}>
          {loading ? "⏳" : "Send ➤"}
        </button>
      </div>
    </form>
  );
}
