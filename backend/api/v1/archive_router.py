from fastapi import APIRouter, Form, HTTPException, Request
from backend.services.upap.engine.upap_engine import engine

router = APIRouter(prefix="/upap")


@router.post("/archive")
def archive_record(
    request: Request,
    record_id: str = Form(...)
):
    # 🔐 Auth context MUST come from upstream (middleware / dependency)
    context = request.state.user

    if not context:
        raise HTTPException(401, "Authentication required")

    if not context.get("email_verified"):
        raise HTTPException(403, "Email verification required")

    return engine.run_archive(record_id)
