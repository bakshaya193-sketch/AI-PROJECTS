import { useState } from "react";
import { uploadMultipleDocuments } from "../api";

const ACCEPT = ".pdf,.txt,.jpg,.jpeg,.png";

export default function UploadDocument({ onUploadSuccess }) {
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [selectedFiles, setSelectedFiles] = useState([]);

  const handleFileSelect = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);
    setStatus(null);
  };

  const handleUpload = async () => {
    if (selectedFiles.length === 0) return;

    setLoading(true);
    setStatus(null);

    try {
      const res = await uploadMultipleDocuments(selectedFiles);
      const results = res.results || [];
      const succeeded = results.filter((r) => r.status === "success");
      const failed = results.filter((r) => r.status === "error");

      let message = "";
      if (succeeded.length > 0) {
        message += `✅ ${succeeded.length} file(s) uploaded successfully:\n`;
        succeeded.forEach((r) => { message += `  • ${r.file} — ${r.chunks} chunks\n`; });
      }
      if (failed.length > 0) {
        message += `\n❌ ${failed.length} file(s) failed:\n`;
        failed.forEach((r) => { message += `  • ${r.file}: ${r.message}\n`; });
      }

      setStatus({ type: succeeded.length > 0 ? "success" : "error", text: message });
      setSelectedFiles([]);

      // Tell parent to refresh the documents list
      if (succeeded.length > 0 && onUploadSuccess) onUploadSuccess();

    } catch (err) {
      setStatus({ type: "error", text: `❌ Upload failed: ${err.response?.data?.detail || err.message}` });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-container">
      <div className="upload-box">
        <div className="upload-icon">📂</div>
        <h3>Upload Documents</h3>
        <p className="upload-description">
          Select one or multiple files (PDF, TXT, JPG, PNG)
        </p>

        {/* File picker */}
        <label className="upload-input-label">
          <input
            type="file"
            accept={ACCEPT}
            multiple
            onChange={handleFileSelect}
            disabled={loading}
            className="upload-input"
          />
          <span className="upload-button">📁 Select Files</span>
        </label>

        {/* Selected files preview */}
        {selectedFiles.length > 0 && (
          <div className="selected-files">
            <p className="selected-title">📋 Selected ({selectedFiles.length}):</p>
            <ul className="selected-list">
              {selectedFiles.map((f, i) => (
                <li key={i} className="selected-item">
                  📄 {f.name} <span className="file-size">({(f.size / 1024).toFixed(1)} KB)</span>
                </li>
              ))}
            </ul>
            <button
              className="upload-submit-btn"
              onClick={handleUpload}
              disabled={loading}
            >
              {loading ? "⏳ Uploading..." : `📤 Upload ${selectedFiles.length} File(s)`}
            </button>
          </div>
        )}

        {/* Status message */}
        {status && (
          <div className={`upload-message ${status.type}`} style={{ whiteSpace: "pre-wrap", textAlign: "left" }}>
            {status.text}
          </div>
        )}
      </div>

      <div className="upload-info">
        <h4>📋 Guidelines</h4>
        <ul>
          <li>📄 PDF documents</li>
          <li>📝 TXT plain text</li>
          <li>🖼️ JPG / PNG images</li>
          <li>📦 Multiple files at once</li>
          <li>♻️ Re-upload to update a file</li>
          <li>Max 15 MB per file</li>
        </ul>
      </div>
    </div>
  );
}
