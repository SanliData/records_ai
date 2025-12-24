# UTF-8, English only

from fastapi import APIRouter, UploadFile, File, HTTPException
from PIL import UnidentifiedImageError

from backend.services.image.canonical_image import normalize_to_canonical_jpeg
from backend.services.upap.engine.upap_engine import get_upap_engine

router = APIRouter(
    prefix="/upap/upload",
    tags=["upap-upload"],
)


@router.post("/preview")
async def upload_preview(file: UploadFile = File(...)):
    raw_bytes = await file.read()

    try:
        canonical = normalize_to_canonical_jpeg(raw_bytes)
    except UnidentifiedImageError:
        raise HTTPException(
            status_code=400,
            detail="Unsupported or invalid image file"
        )

    engine = get_upap_engine()
    return engine.run_stage(
        "upload",
        {
            "file_bytes": canonical,
            "content_type": "image/jpeg",
        },
    )
