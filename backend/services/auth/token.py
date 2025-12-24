# backend/services/auth/token.py
# UTF-8, English only

import secrets
from datetime import datetime, timedelta

_tokens: dict[str, dict] = {}


def generate_token(user_id: str) -> str:
    token = secrets.token_urlsafe(32)
    _tokens[token] = {
        "user_id": user_id,
        "expires_at": datetime.utcnow() + timedelta(hours=24)
    }
    return token


def verify_token(token: str) -> str | None:
    data = _tokens.get(token)
    if not data:
        return None
    if data["expires_at"] < datetime.utcnow():
        return None
    return data["user_id"]
