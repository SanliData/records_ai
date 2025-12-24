# backend/api/auth/signin.py
# UTF-8, English only

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, EmailStr
from datetime import datetime

from backend.services.auth.password import verify_password
from backend.api.auth.signup import _users

router = APIRouter(prefix="/auth")


class SigninRequest(BaseModel):
    email: EmailStr
    password: str


@router.post("/signin")
def signin(req: SigninRequest):
    for user in _users.values():
        if user.email == req.email:
            if not verify_password(req.password, user.password_hash):
                break

            user.last_login_at = datetime.utcnow()
            return {
                "status": "ok",
                "user_id": user.id,
                "email_verified": user.email_verified
            }

    raise HTTPException(401, "Invalid credentials")
