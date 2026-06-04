"""
Config/branding endpoint.
GET /config  - public (used by frontend to load theme)
PUT /config  - admin only
"""
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from typing import Optional
from database import get_db_connection
from routes.auth import require_admin

router = APIRouter()


class ConfigUpdate(BaseModel):
    primary_color: Optional[str] = None
    company_name: Optional[str] = None
    logo_url: Optional[str] = None
    notification_email: Optional[str] = None
    slack_webhook: Optional[str] = None
    font_family: Optional[str] = None


@router.get("/config")
def get_config():
    """Return all config key-value pairs (public)."""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT key, value FROM config")
    result = {row["key"]: row["value"] for row in cur.fetchall()}
    conn.close()
    return result


@router.put("/config")
def update_config(updates: ConfigUpdate, current_user: dict = Depends(require_admin)):
    """Update config values (admin only)."""
    conn = get_db_connection()
    for key, value in updates.model_dump(exclude_none=True).items():
        conn.execute("UPDATE config SET value = ? WHERE key = ?", (value, key))
    conn.commit()
    conn.close()
    return {"message": "Config updated successfully"}
