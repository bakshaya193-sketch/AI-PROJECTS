"""
Site-wide access gate.
A single password that protects the whole app before any page is shown.
The password is read from the SITE_PASSWORD environment variable so it is
never exposed in the frontend code.
"""
import os
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

# Default password if SITE_PASSWORD is not set in .env
DEFAULT_SITE_PASSWORD = "welcome123"


class AccessCheck(BaseModel):
    password: str


@router.post("/verify-access")
def verify_access(body: AccessCheck):
    """Check the site access password. Returns {valid: true} on success."""
    correct = os.getenv("SITE_PASSWORD", DEFAULT_SITE_PASSWORD)
    if body.password == correct:
        return {"valid": True}
    raise HTTPException(status_code=401, detail="Incorrect access password")
