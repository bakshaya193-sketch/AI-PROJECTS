import axios from "axios";

const BASE = "http://localhost:8000";

const api = axios.create({ baseURL: BASE });

// Attach JWT token to every request if present
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Bearer ${token}`;
  return config;
});

// ── Auth ──────────────────────────────────────────────────────────────────
export const login = async (username, password) => {
  const form = new URLSearchParams({ username, password });
  const res = await api.post("/auth/login", form, {
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
  });
  return res.data;
};

export const getMe = () => api.get("/auth/me").then((r) => r.data);

// ── Chat ──────────────────────────────────────────────────────────────────
export const sendChatMessage = (question, sessionId, languageOverride, userId) =>
  api.post("/chat", { question, session_id: sessionId, language_override: languageOverride, user_id: userId }).then((r) => r.data);

export const getMessagesByUser = (userId) =>
  api.get(`/conversations/user/${userId}/messages`).then((r) => r.data);

export const getConversationMessages = (sessionId) =>
  api.get(`/conversations/${sessionId}/messages`).then((r) => r.data);

// ── Upload ────────────────────────────────────────────────────────────────
export const uploadDocument = async (file) => {
  const form = new FormData();
  form.append("file", file);
  const res = await api.post("/upload", form, { headers: { "Content-Type": "multipart/form-data" } });
  return res.data;
};

export const uploadMultipleDocuments = async (files) => {
  const form = new FormData();
  files.forEach((file) => form.append("files", file));
  const res = await api.post("/upload-multiple", form, { headers: { "Content-Type": "multipart/form-data" } });
  return res.data;
};

export const getDocuments = () =>
  api.get("/documents").then((r) => r.data);

export const deleteDocument = (filename) =>
  api.delete(`/documents/${encodeURIComponent(filename)}`).then((r) => r.data);

// ── Tickets ───────────────────────────────────────────────────────────────
export const getTickets = (status) =>
  api.get("/tickets", { params: status ? { status } : {} }).then((r) => r.data);

export const updateTicketStatus = (id, status) =>
  api.patch(`/tickets/${id}`, { status }).then((r) => r.data);

export const getTicketConversation = (id) =>
  api.get(`/tickets/${id}/conversation`).then((r) => r.data);

export const getTicketSession = (id) =>
  api.get(`/tickets/${id}/conversation-session`).then((r) => r.data);

// ── Agent ─────────────────────────────────────────────────────────────────
export const getEscalatedTickets = () =>
  api.get("/agent/tickets").then((r) => r.data);

export const getAgentSuggestion = (ticketId) =>
  api.get(`/agent/tickets/${ticketId}/suggest`).then((r) => r.data);

export const sendAgentReply = (ticketId, message) =>
  api.post(`/agent/tickets/${ticketId}/reply`, { message }).then((r) => r.data);

export const summarizeTicket = (ticketId) =>
  api.post(`/agent/tickets/${ticketId}/summarize`).then((r) => r.data);

export const getConversationStatus = (sessionId) =>
  api.get(`/conversations/${sessionId}/status`).then((r) => r.data);

export const agentJoinChat = (sessionId, agentName) =>
  api.post(`/conversations/${sessionId}/agent/join-named?agent_name=${encodeURIComponent(agentName)}`).then((r) => r.data);

export const agentLeaveChat = (sessionId) =>
  api.post(`/conversations/${sessionId}/agent/leave`).then((r) => r.data);

// ── Analytics ─────────────────────────────────────────────────────────────
export const getAnalytics = () =>
  api.get("/analytics").then((r) => r.data);

// ── Config ────────────────────────────────────────────────────────────────
export const getConfig = () =>
  api.get("/config").then((r) => r.data);

export const updateConfig = (data) =>
  api.put("/config", data).then((r) => r.data);

// ── Site access gate ──────────────────────────────────────────────────────
export const verifyAccess = (password) =>
  api.post("/verify-access", { password }).then((r) => r.data);

// ── Health ────────────────────────────────────────────────────────────────
export const healthCheck = () =>
  api.get("/health").then((r) => r.data);

export default api;
