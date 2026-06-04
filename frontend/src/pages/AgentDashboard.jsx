import { useState, useEffect, useRef } from "react";
import {
  getEscalatedTickets, getAgentSuggestion, sendAgentReply,
  summarizeTicket, updateTicketStatus, getTicketConversation,
  getTicketSession, agentJoinChat, agentLeaveChat, getConversationStatus,
} from "../api";

const POLL_MS = 4000;

export default function AgentDashboard() {
  const [tickets, setTickets] = useState([]);
  const [selected, setSelected] = useState(null);
  const [conversation, setConversation] = useState([]);
  const [suggestion, setSuggestion] = useState("");
  const [reply, setReply] = useState("");
  const [loading, setLoading] = useState(false);
  const [inChat, setInChat] = useState(false); // agent currently in this chat
  const [sessionId, setSessionId] = useState(null);
  const pollRef = useRef(null);
  const bottomRef = useRef(null);
  const user = JSON.parse(localStorage.getItem("user") || "{}");

  useEffect(() => { fetchTickets(); }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [conversation]);

  // Poll for new messages when agent is in a chat
  useEffect(() => {
    if (inChat && selected) {
      pollRef.current = setInterval(() => refreshConversation(selected.id), POLL_MS);
    } else {
      clearInterval(pollRef.current);
    }
    return () => clearInterval(pollRef.current);
  }, [inChat, selected]);

  const fetchTickets = async () => {
    try { setTickets(await getEscalatedTickets()); } catch (e) { console.error(e); }
  };

  const selectTicket = async (ticket) => {
    setSelected(ticket);
    setSuggestion("");
    setInChat(false);
    setSessionId(null);
    clearInterval(pollRef.current);
    try {
      const msgs = await getTicketConversation(ticket.id);
      setConversation(msgs);
      // fetch session_id for join/leave
      const res = await getTicketSession(ticket.id).catch(() => null);
      if (res?.session_id) {
        setSessionId(res.session_id);
        // Sync join state from backend so the Leave button persists if already joined
        const status = await getConversationStatus(res.session_id).catch(() => null);
        if (status?.agent_active) setInChat(true);
      }
    } catch (e) { setConversation([]); }
  };

  const refreshConversation = async (ticketId) => {
    try {
      const msgs = await getTicketConversation(ticketId);
      setConversation(msgs);
    } catch (e) {}
  };

  const handleJoinChat = async () => {
    if (!sessionId) {
      alert("No active session found for this ticket.");
      return;
    }
    try {
      await agentJoinChat(sessionId, user.username || "Support Agent");
      setInChat(true);
      await refreshConversation(selected.id);
    } catch (e) { alert("Could not join chat: " + (e.response?.data?.detail || e.message)); }
  };

  const handleLeaveChat = async () => {
    if (!sessionId) return;
    try {
      await agentLeaveChat(sessionId);
      setInChat(false);
      clearInterval(pollRef.current);
      await refreshConversation(selected.id);
    } catch (e) { alert("Could not leave chat."); }
  };

  const loadSuggestion = async () => {
    if (!selected) return;
    setLoading(true);
    try { setSuggestion((await getAgentSuggestion(selected.id)).suggestion); }
    catch (e) { setSuggestion("Could not load suggestion"); }
    finally { setLoading(false); }
  };

  const handleReply = async () => {
    if (!reply.trim() || !selected) return;
    try {
      await sendAgentReply(selected.id, reply);
      setConversation((c) => [...c, { sender: "agent", content: reply, sentiment: "neutral" }]);
      setReply("");
    } catch (e) { alert(e.response?.data?.detail || "Reply failed"); }
  };

  const handleSummarize = async () => {
    if (!selected) return;
    try {
      const res = await summarizeTicket(selected.id);
      setSelected({ ...selected, summary: res.summary });
    } catch (e) { alert("Summarize failed"); }
  };

  const handleResolve = async () => {
    if (!selected) return;
    if (inChat) await handleLeaveChat();
    try {
      await updateTicketStatus(selected.id, "resolved");
      setTickets((t) => t.filter((tk) => tk.id !== selected.id));
      setSelected(null);
      setConversation([]);
      setInChat(false);
    } catch (e) { alert("Resolve failed"); }
  };

  const SENDER_COLOR = { user: "#2563eb", bot: "#10b981", agent: "#f59e0b", system: "#9ca3af" };

  const renderMsg = (msg, i) => {
    if (msg.sender === "system") {
      return (
        <div key={i} className="system-msg-agent">
          <span>— {msg.content} —</span>
        </div>
      );
    }
    return (
      <div key={i} className="agent-msg" style={{ borderLeftColor: SENDER_COLOR[msg.sender] || "#ccc" }}>
        <span className="agent-msg-sender" style={{ color: SENDER_COLOR[msg.sender] }}>
          {msg.sender.toUpperCase()}
        </span>
        <p>{msg.content}</p>
      </div>
    );
  };

  return (
    <div className="agent-page">
      <div className="agent-header">
        <h1>🧑‍💼 Agent Dashboard</h1>
        <p>Manage customer conversations and provide support</p>
      </div>

      <div className="agent-layout">
        {/* Ticket list */}
        <div className="agent-ticket-list">
          <h3>📋 Open Tickets ({tickets.length})</h3>
          <button onClick={fetchTickets} className="refresh-btn" style={{ marginBottom: 12 }}>🔄 Refresh</button>
          {tickets.length === 0 ? <p className="no-tickets">No open tickets 🎉</p> : (
            tickets.map((t) => (
              <div key={t.id}
                className={`agent-ticket-item ${selected?.id === t.id ? "selected" : ""}`}
                onClick={() => selectTicket(t)}
              >
                <div className="agent-ticket-id">#{t.id}</div>
                <p className="agent-ticket-q">{t.question?.slice(0, 80)}...</p>
                <span className={`ticket-status-badge ${t.status}`}>{t.status?.replace("_", " ")}</span>
              </div>
            ))
          )}
        </div>

        {/* Ticket detail */}
        <div className="agent-detail">
          {!selected ? (
            <div className="empty-state" style={{ padding: "3rem" }}>
              <p>👈 Select a ticket to view conversation</p>
            </div>
          ) : (
            <>
              <div className="agent-detail-header">
                <h3>Ticket #{selected.id}</h3>
                <div className="agent-actions">
                  {/* Join / Leave Chat buttons */}
                  {!inChat ? (
                    <button onClick={handleJoinChat} className="join-chat-btn">
                      🟢 Join Chat
                    </button>
                  ) : (
                    <button onClick={handleLeaveChat} className="leave-chat-btn">
                      🔴 Leave Chat
                    </button>
                  )}
                  <button onClick={loadSuggestion} className="suggest-btn" disabled={loading}>
                    {loading ? "⏳" : "💡 AI Suggest"}
                  </button>
                  <button onClick={handleSummarize} className="summarize-btn">📝 Summarize</button>
                  <button onClick={handleResolve} className="resolve-btn">✅ Resolve</button>
                </div>
              </div>

              {/* Status indicator */}
              {inChat && (
                <div className="in-chat-banner">
                  🟢 You are live in this chat — customer messages appear here in real time
                </div>
              )}

              <p className="agent-question"><b>Issue:</b> {selected.question}</p>
              {selected.summary && <p className="agent-summary">📝 <b>Summary:</b> {selected.summary}</p>}

              {/* Conversation */}
              <div className="agent-conversation">
                {conversation.map((msg, i) => renderMsg(msg, i))}
                <div ref={bottomRef} />
              </div>

              {/* AI suggestion */}
              {suggestion && (
                <div className="suggestion-box">
                  <h4>💡 AI Suggestion:</h4>
                  <pre>{suggestion}</pre>
                </div>
              )}

              {/* Reply box */}
              <div className="agent-reply-box">
                <textarea
                  value={reply}
                  onChange={(e) => setReply(e.target.value)}
                  placeholder={inChat ? "Type your reply to the customer..." : "Join the chat first to reply"}
                  rows={3}
                  disabled={!inChat}
                />
                <button onClick={handleReply} className="send-reply-btn" disabled={!reply.trim() || !inChat}>
                  Send Reply ➤
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  );
}
