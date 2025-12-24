# UTF-8, English only

from fastapi import APIRouter, Request, HTTPException
from backend.services.upap.engine.upap_engine import get_upap_engine

router = APIRouter(
    prefix="/upap",
    tags=["upap-publish"],
)


@router.post("/publish")
def publish_record(request: Request, record_id: str):
    user = request.state.user

    if not user:
        raise HTTPException(401, "Authentication required")
    if not user.get("email_verified"):
        raise HTTPException(403, "Email verification required")

    engine = get_upap_engine()
    return engine.run_publish(record_id, user)
