import { useState, useEffect } from "react";
import { getDocuments, deleteDocument } from "../api";

const FILE_ICON = { pdf: "📕", txt: "📄", image: "🖼️" };

function formatSize(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)} KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)} MB`;
}

function formatDate(dateStr) {
  return new Date(dateStr).toLocaleString();
}

export default function DocumentsList({ refreshTrigger }) {
  const [docs, setDocs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deleting, setDeleting] = useState(null);

  const fetchDocs = async () => {
    setLoading(true);
    try {
      const data = await getDocuments();
      setDocs(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  // Refresh whenever a new file is uploaded
  useEffect(() => { fetchDocs(); }, [refreshTrigger]);

  const handleDelete = async (filename) => {
    if (!window.confirm(`Delete "${filename}"? This will remove it from the AI knowledge base.`)) return;
    setDeleting(filename);
    try {
      await deleteDocument(filename);
      setDocs((d) => d.filter((doc) => doc.filename !== filename));
    } catch (e) {
      alert(e.response?.data?.detail || "Delete failed");
    } finally {
      setDeleting(null);
    }
  };

  return (
    <div className="docs-list-container">
      <div className="docs-list-header">
        <h3>📚 Uploaded Documents ({docs.length})</h3>
        <button className="refresh-btn" onClick={fetchDocs} disabled={loading}>
          🔄 Refresh
        </button>
      </div>

      {loading ? (
        <p className="docs-loading">⏳ Loading documents...</p>
      ) : docs.length === 0 ? (
        <div className="docs-empty">
          <p>📭 No documents uploaded yet.</p>
          <p>Upload PDF, TXT, or image files above to get started.</p>
        </div>
      ) : (
        <div className="docs-table-wrapper">
          <table className="docs-table">
            <thead>
              <tr>
                <th>File</th>
                <th>Type</th>
                <th>Size</th>
                <th>Chunks</th>
                <th>Uploaded</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {docs.map((doc) => (
                <tr key={doc.id} className="docs-row">
                  <td className="docs-filename">
                    <span className="docs-icon">{FILE_ICON[doc.file_type] || "📄"}</span>
                    {doc.filename}
                  </td>
                  <td>
                    <span className="docs-type-badge">{doc.file_type.toUpperCase()}</span>
                  </td>
                  <td className="docs-size">{formatSize(doc.file_size)}</td>
                  <td className="docs-chunks">{doc.chunks_count} chunks</td>
                  <td className="docs-date">{formatDate(doc.uploaded_date)}</td>
                  <td>
                    <button
                      className="docs-delete-btn"
                      onClick={() => handleDelete(doc.filename)}
                      disabled={deleting === doc.filename}
                      title={`Delete ${doc.filename}`}
                    >
                      {deleting === doc.filename ? "⏳" : "🗑️ Delete"}
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  );
}
