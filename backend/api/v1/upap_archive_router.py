# -*- coding: utf-8 -*-
# UTF-8, English only

from fastapi import APIRouter, Request, HTTPException
from backend.services.upap.engine.upap_engine import get_upap_engine

router = APIRouter(
    prefix="/upap/archive",
    tags=["upap-archive"],
)


@router.post("/commit")
def commit_archive(request: Request, record_id: str):
    """
    Commit preview record into user archive.
    State-changing operation → email_verified REQUIRED.
    """
    user_context = request.state.user

    if not user_context:
        raise HTTPException(status_code=401, detail="Authentication required")

    if not user_context.get("email_verified"):
        raise HTTPException(status_code=403, detail="Email verification required")

    engine = get_upap_engine()
    return engine.run_stage(
        "archive",
        {
            "record_id": record_id,
            "user_context": user_context,
        }
    )


@router.get("/my")
def list_my_archive(request: Request):
    """
    List records in the authenticated user's archive.
    Read operation but still requires verified identity.
    """
    user_context = request.state.user

    if not user_context:
        raise HTTPException(status_code=401, detail="Authentication required")

    if not user_context.get("email_verified"):
        raise HTTPException(status_code=403, detail="Email verification required")

    # Minimal placeholder: real implementation will query user archive store
    return {
        "status": "ok",
        "scope": "user",
        "user_id": user_context.get("user_id"),
        "records": [],
    }
