import { useState, useEffect } from "react";
import { getTickets, updateTicketStatus } from "../api";

const PRIORITY_COLOR = { high: "#ef4444", normal: "#f59e0b", low: "#10b981" };

export default function TicketsPage() {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [filter, setFilter] = useState("all");

  const fetchTickets = async () => {
    setLoading(true);
    try {
      const data = await getTickets(filter === "all" ? null : filter);
      setTickets(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetchTickets(); }, [filter]);

  const resolve = async (id) => {
    try {
      await updateTicketStatus(id, "resolved");
      setTickets((t) => t.filter((tk) => tk.id !== id));
    } catch (e) {
      alert(e.response?.data?.detail || "Please login to update tickets");
    }
  };

  const fmt = (d) => new Date(d).toLocaleString();

  return (
    <div className="tickets-page">
      <div className="tickets-header">
        <div>
          <h1>🎫 Support Tickets</h1>
          <p>Customer questions that need human attention</p>
        </div>
        <div className="tickets-controls">
          <select value={filter} onChange={(e) => setFilter(e.target.value)} className="filter-select">
            <option value="all">All open</option>
            <option value="unresolved">Unresolved</option>
            <option value="pending_agent">Pending Agent</option>
          </select>
          <button className="refresh-btn" onClick={fetchTickets} disabled={loading}>🔄 Refresh</button>
        </div>
      </div>

      {loading ? (
        <div className="loading-state">⏳ Loading tickets...</div>
      ) : tickets.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">✨</div>
          <h2>No Tickets!</h2>
          <p>All customer questions have been answered.</p>
        </div>
      ) : (
        <div className="tickets-list">
          {tickets.map((t) => (
            <div key={t.id} className="ticket-card">
              <div className="ticket-header">
                <span className="ticket-id">#{t.id}</span>
                <span className="ticket-priority" style={{ color: PRIORITY_COLOR[t.priority] }}>
                  ● {t.priority?.toUpperCase()}
                </span>
                <span className={`ticket-status-badge ${t.status}`}>{t.status.replace("_", " ")}</span>
              </div>
              <p className="ticket-question">{t.question}</p>
              {t.summary && <p className="ticket-summary">📝 {t.summary}</p>}
              <div className="ticket-footer">
                <span className="ticket-date">📅 {fmt(t.created_date)}</span>
                <button className="resolve-btn" onClick={() => resolve(t.id)}>✅ Mark Resolved</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
