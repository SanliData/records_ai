# backend/api/auth/verify.py
# UTF-8, English only

from fastapi import APIRouter, HTTPException
from backend.services.auth.token import verify_token
from backend.api.auth.signup import _users

router = APIRouter(prefix="/auth")


@router.get("/verify")
def verify_email(token: str):
    user_id = verify_token(token)

    if not user_id or user_id not in _users:
        raise HTTPException(400, "Invalid or expired token")

    _users[user_id].email_verified = True

    return {"status": "verified"}
