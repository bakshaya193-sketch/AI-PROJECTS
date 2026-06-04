import { useState, useEffect, useRef } from "react";
import ChatBox from "../components/ChatBox";
import MessageBubble from "../components/MessageBubble";
import LanguageSelector from "../components/LanguageSelector";
import { sendChatMessage, getConversationMessages, getMessagesByUser, getConversationStatus } from "../api";

const POLL_MS = 4000;

// Each identity gets its OWN localStorage key so guests and customers
// can never see each other's conversation.
function sessionKeyFor(user) {
  if (user?.role === "customer" && user?.id) return `support_session_user_${user.id}`;
  return "support_session_guest";
}

export default function ChatPage({ user }) {
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);
  const [sessionId, setSessionId] = useState(null);
  const [langOverride, setLangOverride] = useState(null);
  const [detectedLang, setDetectedLang] = useState(null);
  const [agentActive, setAgentActive] = useState(false);
  const [agentName, setAgentName] = useState(null);
  const [hasAgentReply, setHasAgentReply] = useState(false);
  const bottomRef = useRef(null);
  const pollRef = useRef(null);
  const prevAgentActive = useRef(false);

  const storageKey = sessionKeyFor(user);

  useEffect(() => { bottomRef.current?.scrollIntoView({ behavior: "smooth" }); }, [messages]);

  // Whenever the logged-in identity changes, fully reset and load THAT identity's chat
  useEffect(() => {
    // Reset everything first so no previous user's messages linger
    clearInterval(pollRef.current);
    setMessages([]);
    setSessionId(null);
    setAgentActive(false);
    setAgentName(null);
    setHasAgentReply(false);
    prevAgentActive.current = false;

    if (user?.role === "customer" && user?.id) {
      // Logged-in customer → load their conversation by user_id (server-side, private)
      loadByUserId(user.id);
    } else {
      // Guest → only use the guest-namespaced session
      const sid = localStorage.getItem("support_session_guest");
      if (sid) {
        setSessionId(sid);
        loadBySession(sid);
      }
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [user?.id, user?.role]);

  // Poll for new messages + agent status
  useEffect(() => {
    if (sessionId) {
      pollRef.current = setInterval(() => pollUpdates(sessionId), POLL_MS);
    }
    return () => clearInterval(pollRef.current);
  }, [sessionId]);

  const dbMsgToUi = (msg) => ({
    type: msg.sender === "user" ? "user" : "ai",
    sender: msg.sender,
    text: msg.content,
    sentiment: msg.sentiment,
    sentiment_score: msg.sentiment_score,
    detectedLanguage: msg.language !== "en" ? msg.language : null,
    sources: [], ticketCreated: false, escalated: false,
  });

  const loadByUserId = async (uid) => {
    try {
      const data = await getMessagesByUser(uid);
      if (data.session_id) {
        setSessionId(data.session_id);
        localStorage.setItem(`support_session_user_${uid}`, data.session_id);
      }
      if (data.messages?.length > 0) {
        setMessages(data.messages.map(dbMsgToUi));
        if (data.messages.some((m) => m.sender === "agent")) setHasAgentReply(true);
      }
    } catch (e) { console.error(e); }
  };

  const loadBySession = async (sid) => {
    try {
      const msgs = await getConversationMessages(sid);
      if (msgs.length > 0) {
        setMessages(msgs.map(dbMsgToUi));
        if (msgs.some((m) => m.sender === "agent")) setHasAgentReply(true);
      }
    } catch (e) { console.error(e); }
  };

  const pollUpdates = async (sid) => {
    try {
      const status = await getConversationStatus(sid);
      const nowActive = status.agent_active;

      if (nowActive && !prevAgentActive.current) {
        setAgentActive(true);
        setAgentName(status.agent_name);
        prevAgentActive.current = true;
      }
      if (!nowActive && prevAgentActive.current) {
        setAgentActive(false);
        setAgentName(null);
        prevAgentActive.current = false;
      }

      const msgs = await getConversationMessages(sid);
      setMessages((prev) => {
        if (msgs.length !== prev.length) {
          if (msgs.some((m) => m.sender === "agent")) setHasAgentReply(true);
          return msgs.map(dbMsgToUi);
        }
        return prev;
      });
    } catch (e) {}
  };

  const handleSend = async (question) => {
    setMessages((m) => [...m, { type: "user", sender: "user", text: question }]);
    setLoading(true);
    try {
      const userId = user?.role === "customer" ? user.id : null;
      const res = await sendChatMessage(question, sessionId, langOverride, userId);
      if (!sessionId) {
        setSessionId(res.session_id);
        // Save under THIS identity's namespaced key only
        localStorage.setItem(storageKey, res.session_id);
      }
      setDetectedLang(res.detected_language);

      if (res.routed_to_agent) {
        setLoading(false);
        return;
      }

      setMessages((m) => [...m, {
        type: "ai", sender: "bot",
        text: res.answer,
        ticketCreated: res.ticket_created,
        ticketId: res.ticket_id,
        detectedLanguage: res.detected_language !== "en" ? res.detected_language : null,
        escalated: res.escalated,
        sources: [], sentiment: null,
      }]);
    } catch (err) {
      setMessages((m) => [...m, { type: "ai", sender: "bot", text: "❌ Server error. Please try again." }]);
    } finally {
      setLoading(false);
    }
  };

  const handleNewChat = () => {
    if (!window.confirm("End this chat and start a new one?")) return;
    localStorage.removeItem(storageKey);
    clearInterval(pollRef.current);
    setSessionId(null);
    setMessages([]);
    setAgentActive(false);
    setHasAgentReply(false);
    prevAgentActive.current = false;
  };

  return (
    <div className="chat-page">
      <div className="chat-header">
        <div className="chat-header-top">
          <div>
            <h1>💬 Customer Support Chat</h1>
            <p>Ask anything about our products and services</p>
          </div>
          {messages.length > 0 && (
            <button className="new-chat-btn" onClick={handleNewChat}>🔄 New Chat</button>
          )}
        </div>
        <div className="chat-header-controls">
          <LanguageSelector value={langOverride || ""} onChange={setLangOverride} />
          {detectedLang && detectedLang !== "en" && (
            <span className="detected-lang-badge">🌐 {detectedLang.toUpperCase()}</span>
          )}
          {agentActive && (
            <span className="agent-active-badge">🟢 {agentName || "Agent"} is here</span>
          )}
          {!agentActive && hasAgentReply && (
            <span className="agent-replied-badge">🧑‍💼 Agent replied</span>
          )}
        </div>
      </div>

      {agentActive && (
        <div className="agent-connected-banner">
          🟢 You are now chatting with <b>{agentName || "a support agent"}</b>. Your messages go directly to them.
        </div>
      )}

      <div className="chat-messages">
        {messages.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🤖</div>
            <h2>Welcome{user?.username ? `, ${user.username}` : ""}!</h2>
            <p>Ask me anything about our products, shipping, refunds, or services.</p>
            <p className="empty-hint">
              {user?.role === "customer"
                ? "Your conversation is private and saved to your account."
                : "Log in to save your conversation across visits."}
            </p>
          </div>
        ) : (
          messages.map((msg, i) => <MessageBubble key={i} message={msg} />)
        )}
        <div ref={bottomRef} />
      </div>

      <div className="chat-input-area">
        {agentActive && (
          <p className="routing-label">📨 Sending to agent: <b>{agentName}</b></p>
        )}
        <ChatBox onSend={handleSend} loading={loading} />
      </div>
    </div>
  );
}
