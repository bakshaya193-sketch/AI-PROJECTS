import { useState } from "react";
import { verifyAccess } from "../api";

/**
 * Full-screen password gate shown before the app loads.
 * The user must enter the correct site password to enter.
 */
export default function SiteGate({ onUnlock, companyName }) {
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError("");
    try {
      await verifyAccess(password);
      // Remember for this browser session so internal navigation doesn't re-prompt
      sessionStorage.setItem("site_unlocked", "yes");
      onUnlock();
    } catch (err) {
      if (err.response?.status === 401) {
        setError("Incorrect password. Please try again.");
      } else {
        setError("Cannot reach the server. Make sure the backend is running.");
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="site-gate">
      <div className="site-gate-card">
        <div className="site-gate-icon">🔒</div>
        <h1>{companyName || "AI Customer Support"}</h1>
        <p className="site-gate-subtitle">This site is private. Please enter the access password to continue.</p>

        <form onSubmit={handleSubmit} className="site-gate-form">
          <input
            type="password"
            placeholder="Enter access password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            autoFocus
          />
          {error && <p className="site-gate-error">❌ {error}</p>}
          <button type="submit" disabled={loading} className="site-gate-btn">
            {loading ? "Checking..." : "🔓 Unlock"}
          </button>
        </form>

        <p className="site-gate-footer">Protected access · Authorized users only</p>
      </div>
    </div>
  );
}
