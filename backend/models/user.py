# backend/models/user.py
# UTF-8, English only

from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class User(BaseModel):
    id: str
    email: EmailStr
    password_hash: str

    # 🔒 Archive / Publish gate
    email_verified: bool = False

    created_at: datetime
    last_login_at: Optional[datetime] = None
