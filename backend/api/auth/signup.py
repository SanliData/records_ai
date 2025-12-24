# backend/api/auth/signup.py
# UTF-8, English only

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime
import uuid

from backend.models.user import User
from backend.services.auth.password import hash_password
from backend.services.auth.token import generate_token
from backend.services.email.sender import send_verification_email

_users: dict[str, User] = {}

router = APIRouter(prefix="/auth")


class SignupRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signup")
def signup(req: SignupRequest):
    if any(u.email == req.email for u in _users.values()):
        raise HTTPException(400, "Email already exists")

    user = User(
        id=str(uuid.uuid4()),
        email=req.email,
        password_hash=hash_password(req.password),
        email_verified=False,
        created_at=datetime.utcnow()
    )

    _users[user.id] = user

    token = generate_token(user.id)
    verify_url = f"/auth/verify?token={token}"

    send_verification_email(user.email, verify_url)

    return {
        "status": "created",
        "message": "Verification email sent"
    }
