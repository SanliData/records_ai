# backend/services/auth/guards.py
# UTF-8, English only

from fastapi import HTTPException
from backend.api.auth.signup import _users


def require_verified_user(user_id: str):
    user = _users.get(user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    if not user.email_verified:
        raise HTTPException(
            status_code=403,
            detail="Email verification required"
        )

    return user
