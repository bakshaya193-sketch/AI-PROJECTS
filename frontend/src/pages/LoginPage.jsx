import { useState } from "react";
import { login } from "../api";

const PAGE_INFO = {
  admin:     { label: "Admin Login",    hint: "Admin access only",               icon: "👑" },
  agent:     { label: "Staff Login",    hint: "Agent or Admin credentials",      icon: "🧑‍💼" },
  analytics: { label: "Staff Login",    hint: "Agent or Admin credentials",      icon: "📊" },
  tickets:   { label: "Staff Login",    hint: "Agent or Admin credentials",      icon: "🎫" },
  customer:  { label: "Customer Login", hint: "Login to save your chat history",  icon: "👤" },
};

// Which roles are allowed to log in from each login page
const ALLOWED_ROLES = {
  customer:  ["customer"],
  agent:     ["agent", "admin"],
  analytics: ["agent", "admin"],
  tickets:   ["agent", "admin"],
  admin:     ["admin"],
};

export default function LoginPage({ onLogin, requiredPage }) {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const info = PAGE_INFO[requiredPage] || { label: "Login", hint: "Enter your credentials", icon: "🔐" };
  const isCustomerPage = requiredPage === "customer";

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      const data = await login(form.username, form.password);

      // Enforce that the account's role matches this login page
      const allowed = ALLOWED_ROLES[requiredPage] || ["customer", "agent", "admin"];
      if (!allowed.includes(data.role)) {
        if (isCustomerPage) {
          setError("This is a customer account page. Staff must use the Staff Login.");
        } else if (data.role === "customer") {
          setError("Customer accounts must use the Customer Login page.");
        } else {
          setError("Your account does not have access to this page.");
        }
        setLoading(false);
        return; // do NOT log in — token is never stored
      }

      onLogin({ username: data.username, role: data.role, id: data.user_id }, data.access_token);
    } catch (err) {
      setError(err.response?.data?.detail || "Invalid username or password");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-card">
        <div className="login-icon">{info.icon}</div>
        <h2>{info.label}</h2>
        <p className="login-hint">{info.hint}</p>

        {/* Make it clear which accounts belong here */}
        <div className="login-scope-note">
          {isCustomerPage
            ? "👤 For customers only"
            : "🔒 For staff (admin / agent) only"}
        </div>

        <form onSubmit={handleSubmit} className="login-form">
          <input
            type="text"
            placeholder="Username"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
            required
            autoFocus
          />
          <input
            type="password"
            placeholder="Password"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
            required
          />
          {error && <p className="login-error">❌ {error}</p>}
          <button type="submit" disabled={loading} className="login-submit">
            {loading ? "Logging in..." : "Login"}
          </button>
        </form>
      </div>
    </div>
  );
}
