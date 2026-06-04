import { useState, useEffect } from "react";
import Navigation from "./components/Navigation";
import ChatPage from "./pages/ChatPage";
import AdminPage from "./pages/AdminPage";
import TicketsPage from "./pages/TicketsPage";
import AgentDashboard from "./pages/AgentDashboard";
import AnalyticsDashboard from "./pages/AnalyticsDashboard";
import LoginPage from "./pages/LoginPage";
import SiteGate from "./components/SiteGate";
import { healthCheck, getConfig } from "./api";
import "./styles/App.css";

const ACCESS = {
  chat:           ["guest", "customer", "admin"],
  "customer-login": ["guest"],
  login:          ["guest", "customer", "agent", "admin"],
  tickets:        ["agent", "admin"],
  agent:          ["agent", "admin"],
  analytics:      ["agent", "admin"],
  admin:          ["admin"],
};

export default function App() {
  const [page, setPage] = useState("chat");
  const [connected, setConnected] = useState(false);
  const [user, setUser] = useState(null);
  const [config, setConfig] = useState({});
  // Site-wide access gate — unlocked for the current browser session
  const [unlocked, setUnlocked] = useState(() => sessionStorage.getItem("site_unlocked") === "yes");

  useEffect(() => {
    // One-time cleanup: remove the legacy shared session key that leaked
    // chats between guest and customers in older versions.
    localStorage.removeItem("support_session_id");

    const saved = localStorage.getItem("user");
    if (saved) {
      const u = JSON.parse(saved);
      setUser(u);
      if (u.role === "admin") setPage("admin");
      else if (u.role === "agent") setPage("agent");
      else setPage("chat"); // customer goes to chat
    }
    healthCheck().then(() => setConnected(true)).catch(() => setConnected(false));
    getConfig().then((cfg) => {
      setConfig(cfg);
      if (cfg.primary_color)
        document.documentElement.style.setProperty("--primary-color", cfg.primary_color);
    }).catch(() => {});
  }, []);

  const handleLogin = (userData, token) => {
    localStorage.setItem("token", token);
    localStorage.setItem("user", JSON.stringify(userData));
    setUser(userData);
    if (userData.role === "admin") setPage("admin");
    else if (userData.role === "agent") setPage("agent");
    else setPage("chat");
  };

  const handleLogout = () => {
    localStorage.removeItem("token");
    localStorage.removeItem("user");
    setUser(null);
    setPage("chat");
  };

  const handleSetPage = (target) => {
    const role = user?.role || "guest";
    const allowed = ACCESS[target] || [];
    if (allowed.includes(role)) {
      setPage(target);
    } else {
      setPage(role === "guest" ? "login" : "chat");
    }
  };

  const renderPage = () => {
    const role = user?.role || "guest";
    const allowed = ACCESS[page] || [];

    if (!allowed.includes(role)) {
      return <LoginPage onLogin={handleLogin} requiredPage={page} />;
    }

    switch (page) {
      case "chat":           return <ChatPage user={user} />;
      case "customer-login": return <LoginPage onLogin={handleLogin} requiredPage="customer" />;
      case "login":          return <LoginPage onLogin={handleLogin} requiredPage="agent" />;
      case "admin":          return <AdminPage />;
      case "tickets":        return <TicketsPage />;
      case "agent":          return <AgentDashboard />;
      case "analytics":      return <AnalyticsDashboard />;
      default:               return <ChatPage user={user} />;
    }
  };

  // Show the password gate first — nothing else renders until unlocked
  if (!unlocked) {
    return <SiteGate onUnlock={() => setUnlocked(true)} companyName={config.company_name} />;
  }

  return (
    <div className="app">
      <Navigation
        page={page}
        setPage={handleSetPage}
        user={user}
        onLogout={handleLogout}
        companyName={config.company_name || "AI Support"}
        logoUrl={config.logo_url || ""}
      />
      {!connected && (
        <div className="connection-warning">
          ⚠️ Backend not connected — it may be starting up (free hosting can take ~50s to wake). Please wait a moment and refresh.
        </div>
      )}
      <main className="main-content">{renderPage()}</main>
      <footer className="app-footer">
        <p>{config.company_name || "AI Customer Support"} · Built with React + FastAPI + OpenAI</p>
        <p className="footer-status">{connected ? "✅ Connected" : "❌ Disconnected"}</p>
      </footer>
    </div>
  );
}
