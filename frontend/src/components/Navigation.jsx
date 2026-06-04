export default function Navigation({ page, setPage, user, onLogout, companyName, logoUrl }) {
  const role = user?.role || "guest";

  const allLinks = [
    { id: "chat",      label: "Chat",      icon: "💬", visibleTo: ["guest", "customer", "admin"] },
    { id: "tickets",   label: "Tickets",   icon: "🎫", visibleTo: ["agent", "admin"] },
    { id: "agent",     label: "Agent",     icon: "🧑‍💼", visibleTo: ["agent", "admin"] },
    { id: "analytics", label: "Analytics", icon: "📊", visibleTo: ["agent", "admin"] },
    { id: "admin",     label: "Admin",     icon: "⚙️",  visibleTo: ["admin"] },
  ];

  const visibleLinks = allLinks.filter((l) => l.visibleTo.includes(role));

  const getRoleBadge = () => {
    if (role === "admin") return "👑";
    if (role === "agent") return "🧑‍💼";
    if (role === "customer") return "👤";
    return "";
  };

  return (
    <nav className="navigation">
      <div className="nav-container">
        <div className="nav-logo">
          {logoUrl && <img src={logoUrl} alt="logo" className="nav-logo-img" />}
          <span className="logo-icon">🤖</span>
          <span className="logo-text">{companyName}</span>
        </div>

        <ul className="nav-links">
          {visibleLinks.map((l) => (
            <li key={l.id}>
              <button
                className={`nav-link ${page === l.id ? "active" : ""}`}
                onClick={() => setPage(l.id)}
              >
                <span>{l.icon}</span> {l.label}
              </button>
            </li>
          ))}
        </ul>

        <div className="nav-auth">
          {user ? (
            <div className="user-info">
              <span className="user-badge">
                {getRoleBadge()} {user.username}
                <span className="role-tag">{role}</span>
              </span>
              <button className="logout-btn" onClick={onLogout}>Logout</button>
            </div>
          ) : (
            <div className="nav-login-btns">
              <button className="customer-login-btn" onClick={() => setPage("customer-login")}>
                👤 Login
              </button>
              <button className="login-btn" onClick={() => setPage("login")}>
                🔒 Staff
              </button>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
}
