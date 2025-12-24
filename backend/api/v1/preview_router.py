# backend/api/v1/preview_router.py
# UTF-8, English only

from fastapi import APIRouter, HTTPException
from backend.storage.preview_store import get_preview_by_id

router = APIRouter(prefix="/preview", tags=["preview"])


@router.get("/{record_id}")
def get_preview(record_id: str):
    preview = get_preview_by_id(record_id)
    if preview is None:
        raise HTTPException(status_code=404, detail="Preview not found")

    return {
        "record_id": preview.record_id,
        "canonical_image_url": preview.canonical_image_url,
        "metadata": preview.metadata,
        "status": preview.status,
    }
