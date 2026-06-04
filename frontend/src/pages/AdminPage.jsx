import { useState, useEffect } from "react";
import UploadDocument from "../components/UploadDocument";
import DocumentsList from "../components/DocumentsList";
import { getConfig, updateConfig } from "../api";

export default function AdminPage() {
  const [cfg, setCfg] = useState({});
  const [saved, setSaved] = useState(false);
  const [uploadTrigger, setUploadTrigger] = useState(0);

  useEffect(() => { getConfig().then(setCfg).catch(() => {}); }, []);

  // Called when a file is uploaded successfully — refreshes the documents list
  const handleUploadSuccess = () => setUploadTrigger((n) => n + 1);

  const handleSave = async (e) => {
    e.preventDefault();
    try {
      await updateConfig(cfg);
      setSaved(true);
      setTimeout(() => setSaved(false), 3000);
      if (cfg.primary_color)
        document.documentElement.style.setProperty("--primary-color", cfg.primary_color);
    } catch (err) {
      alert(err.response?.data?.detail || "Save failed — are you logged in as admin?");
    }
  };

  return (
    <div className="admin-page">
      <div className="admin-header">
        <h1>⚙️ Admin Panel</h1>
        <p>Manage documents, branding, and notification settings</p>
      </div>

      {/* Upload + Config side by side */}
      <div className="admin-grid">
        <section className="admin-card">
          <h2>📂 Upload Documents</h2>
          <UploadDocument onUploadSuccess={handleUploadSuccess} />
        </section>

        <section className="admin-card">
          <h2>🎨 Branding & Config</h2>
          <form className="config-form" onSubmit={handleSave}>
            <label>Company Name
              <input value={cfg.company_name || ""} onChange={(e) => setCfg({ ...cfg, company_name: e.target.value })} />
            </label>
            <label>Primary Color
              <div className="color-row">
                <input type="color" value={cfg.primary_color || "#2563eb"} onChange={(e) => setCfg({ ...cfg, primary_color: e.target.value })} />
                <input value={cfg.primary_color || ""} onChange={(e) => setCfg({ ...cfg, primary_color: e.target.value })} placeholder="#2563eb" />
              </div>
            </label>
            <label>Logo URL
              <input value={cfg.logo_url || ""} onChange={(e) => setCfg({ ...cfg, logo_url: e.target.value })} placeholder="https://..." />
            </label>
            <label>Notification Email
              <input type="email" value={cfg.notification_email || ""} onChange={(e) => setCfg({ ...cfg, notification_email: e.target.value })} placeholder="support@company.com" />
            </label>
            <label>Slack Webhook URL
              <input value={cfg.slack_webhook || ""} onChange={(e) => setCfg({ ...cfg, slack_webhook: e.target.value })} placeholder="https://hooks.slack.com/..." />
            </label>
            <button type="submit" className="save-btn">💾 Save Settings</button>
            {saved && <p className="save-success">✅ Settings saved!</p>}
          </form>
        </section>
      </div>

      {/* Documents list — full width below upload */}
      <section className="admin-card">
        <DocumentsList refreshTrigger={uploadTrigger} />
      </section>

      {/* How it works */}
      <section className="admin-card how-it-works">
        <h2>📖 How It Works</h2>
        <div className="steps-grid">
          {[
            ["1️⃣", "Upload Documents", "Upload PDF, TXT, or images with company information"],
            ["2️⃣", "AI Indexes Content", "Text is extracted, chunked, and stored in vector database"],
            ["3️⃣", "Customers Ask Questions", "AI retrieves relevant chunks and generates accurate answers"],
            ["4️⃣", "Auto Ticket Creation", "Questions the AI can't answer become support tickets automatically"],
          ].map(([num, title, desc]) => (
            <div key={title} className="step-card">
              <div className="step-num">{num}</div>
              <h4>{title}</h4>
              <p>{desc}</p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
