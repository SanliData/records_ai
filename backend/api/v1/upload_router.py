# backend/api/v1/upload_router.py
# UTF-8, English only

from fastapi import APIRouter, UploadFile, File, Form
from typing import Optional

from backend.services.image.canonical_image import normalize_to_canonical_jpeg
from backend.services.upap.engine.upap_engine import upap_engine

router = APIRouter(prefix="/upap")


@router.post("/upload")
async def upload_only(
    file: UploadFile = File(...),
    email: Optional[str] = Form(None)
):
    """
    UPAP – Upload-only entry point (PREVIEW MODE).

    Pipeline:
    1) AuthStage (optional, preview allowed)
    2) UploadStage (canonical JPEG only)

    Rules:
    - Raw image bytes are NEVER persisted
    - Only canonical JPEG enters the system
    """

    # 1) AUTH STAGE (OPTIONAL FOR PREVIEW)
    auth_payload = {"email": email}
    user_context = upap_engine.run_stage("auth", auth_payload)

    # 2) READ RAW FILE (TEMP MEMORY ONLY)
    raw_bytes = await file.read()

    # 3) CANONICAL JPEG NORMALIZATION (MANDATORY)
    canonical_jpeg = normalize_to_canonical_jpeg(raw_bytes)

    # 4) UPLOAD STAGE — ONLY CANONICAL JPEG IS USED
    upload_payload = {
        "file": canonical_jpeg,
        "user_context": user_context,
        "content_type": "image/jpeg",
        "mode": "PREVIEW_ONLY"
    }

    upload_context = upap_engine.run_stage("upload", upload_payload)

    return {
        "status": "ok",
        "mode": "preview",
        "auth": user_context,
        "upload": upload_context
    }
