# backend/api/user/preview_attach.py
# UTF-8, English only

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.api.auth.signup import _users

router = APIRouter(prefix="/user")


class AttachRequest(BaseModel):
    user_id: str
    preview_id: str
    use_custom_image: bool = False


@router.post("/archive/attach")
def attach_preview(req: AttachRequest):
    user = _users.get(req.user_id)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user")

    if not user.email_verified:
        raise HTTPException(
            status_code=403,
            detail="Email verification required"
        )

    return {
        "status": "attached",
        "preview_id": req.preview_id,
        "user_id": req.user_id,
        "custom_image": req.use_custom_image
    }
