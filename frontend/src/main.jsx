import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App.jsx";
import "./styles/App.css";
import "./styles/ChatPage.css";
import "./styles/AdminPage.css";
import "./styles/TicketsPage.css";
import "./styles/AgentDashboard.css";
import "./styles/AnalyticsDashboard.css";
import "./styles/LoginPage.css";

ReactDOM.createRoot(document.getElementById("root")).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>
);
