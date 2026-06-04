import { useState, useEffect } from "react";
import {
  BarChart, Bar, PieChart, Pie, Cell, LineChart, Line,
  XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer,
} from "recharts";
import { getAnalytics } from "../api";

const COLORS = ["#2563eb", "#10b981", "#f59e0b", "#ef4444", "#8b5cf6"];

function StatCard({ icon, label, value, sub }) {
  return (
    <div className="stat-card">
      <div className="stat-icon">{icon}</div>
      <div className="stat-value">{value}</div>
      <div className="stat-label">{label}</div>
      {sub && <div className="stat-sub">{sub}</div>}
    </div>
  );
}

export default function AnalyticsDashboard() {
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const fetch = async () => {
    setLoading(true);
    try {
      const res = await getAnalytics();
      setData(res);
      setError("");
    } catch (e) {
      setError(e.response?.data?.detail || "Failed to load analytics. Please login first.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => { fetch(); }, []);

  if (loading) return <div className="loading-state">⏳ Loading analytics...</div>;
  if (error) return <div className="error-message" style={{ margin: "2rem" }}>❌ {error}</div>;
  if (!data) return null;

  // Prepare chart data
  const sentimentData = Object.entries(data.sentiment_distribution || {}).map(([name, value]) => ({ name, value }));
  const statusData = Object.entries(data.ticket_status_breakdown || {}).map(([name, value]) => ({ name, value }));
  const priorityData = Object.entries(data.tickets_by_priority || {}).map(([name, value]) => ({ name, value }));
  const dailyData = data.daily_conversations || [];
  const langData = data.top_languages || [];

  return (
    <div className="analytics-page">
      <div className="analytics-header">
        <h1>📊 Analytics Dashboard</h1>
        <p>Real-time metrics from your customer support system</p>
        <button onClick={fetch} className="refresh-btn">🔄 Refresh</button>
      </div>

      {/* Stat Cards */}
      <div className="stats-grid">
        <StatCard icon="💬" label="Total Conversations" value={data.total_conversations} />
        <StatCard icon="📩" label="Total Messages" value={data.total_messages} />
        <StatCard icon="🎫" label="Total Tickets" value={data.total_tickets} />
        <StatCard icon="✅" label="Resolved" value={data.resolved_tickets} sub={`${data.resolution_rate}% rate`} />
        <StatCard icon="🔴" label="Escalated" value={data.escalated_conversations} />
        <StatCard icon="💬" label="Avg Msgs/Conv" value={data.avg_messages_per_conversation} />
      </div>

      {/* Charts row 1 */}
      <div className="charts-grid">
        {/* Sentiment Distribution Pie */}
        <div className="chart-card">
          <h3>😊 Sentiment Distribution</h3>
          {sentimentData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={sentimentData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}>
                  {sentimentData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : <p className="no-data">No data yet</p>}
        </div>

        {/* Ticket Status Pie */}
        <div className="chart-card">
          <h3>🎫 Ticket Status</h3>
          {statusData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <PieChart>
                <Pie data={statusData} dataKey="value" nameKey="name" cx="50%" cy="50%" outerRadius={80} label={({ name, value }) => `${name}: ${value}`}>
                  {statusData.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
                </Pie>
                <Tooltip />
              </PieChart>
            </ResponsiveContainer>
          ) : <p className="no-data">No data yet</p>}
        </div>

        {/* Priority Bar Chart */}
        <div className="chart-card">
          <h3>⚡ Tickets by Priority</h3>
          {priorityData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={priorityData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="value" fill="#2563eb" radius={[4, 4, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="no-data">No data yet</p>}
        </div>
      </div>

      {/* Charts row 2 */}
      <div className="charts-grid">
        {/* Daily Conversations Line */}
        <div className="chart-card chart-wide">
          <h3>📈 Conversations Last 7 Days</h3>
          {dailyData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <LineChart data={dailyData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="day" />
                <YAxis />
                <Tooltip />
                <Legend />
                <Line type="monotone" dataKey="count" stroke="#2563eb" strokeWidth={2} dot={{ r: 4 }} name="Conversations" />
              </LineChart>
            </ResponsiveContainer>
          ) : <p className="no-data">No data yet — start chatting to see trends</p>}
        </div>

        {/* Top Languages Bar */}
        <div className="chart-card">
          <h3>🌐 Top Languages</h3>
          {langData.length > 0 ? (
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={langData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis type="category" dataKey="language" />
                <Tooltip />
                <Bar dataKey="count" fill="#10b981" radius={[0, 4, 4, 0]} />
              </BarChart>
            </ResponsiveContainer>
          ) : <p className="no-data">No data yet</p>}
        </div>
      </div>
    </div>
  );
}
