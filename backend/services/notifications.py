"""
Email and Slack notification service.
Reads settings from the config table; gracefully skips if not configured.
"""
import smtplib
import os
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def send_email_notification(to_email: str, subject: str, body: str) -> bool:
    """Send an HTML email via SMTP. Reads SMTP config from environment."""
    smtp_host = os.getenv("SMTP_HOST", "")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    if not smtp_host or not smtp_user:
        print(f"[Email not configured] Subject: {subject}")
        return False

    try:
        msg = MIMEMultipart("alternative")
        msg["From"] = smtp_user
        msg["To"] = to_email
        msg["Subject"] = subject
        msg.attach(MIMEText(body, "html"))

        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.ehlo()
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)

        print(f"[Email sent] {subject} → {to_email}")
        return True
    except Exception as e:
        print(f"[Email error] {e}")
        return False


def send_slack_notification(webhook_url: str, message: str) -> bool:
    """Post a message to Slack via incoming webhook."""
    if not webhook_url:
        return False
    try:
        resp = requests.post(webhook_url, json={"text": message}, timeout=5)
        return resp.status_code == 200
    except Exception as e:
        print(f"[Slack error] {e}")
        return False


def notify_new_ticket(ticket_id: int, question: str, priority: str, notification_email: str, slack_webhook: str):
    """Notify support team of a new ticket via email and/or Slack."""
    emoji = "🔴" if priority == "high" else "🟡"
    subject = f"{emoji} New Support Ticket #{ticket_id}"
    body = f"""
    <h2>{emoji} New Support Ticket #{ticket_id}</h2>
    <p><b>Priority:</b> {priority.upper()}</p>
    <p><b>Question:</b> {question}</p>
    <p>Please review this ticket in the Agent Dashboard.</p>
    """
    if notification_email:
        send_email_notification(notification_email, subject, body)
    if slack_webhook:
        send_slack_notification(slack_webhook, f"{emoji} *Ticket #{ticket_id}* [{priority.upper()}]\n{question}")
