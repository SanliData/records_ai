# backend/models/preview_record.py
# UTF-8, English only

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class PreviewRecord(BaseModel):
    preview_id: str
    canonical_image_path: str
    detected_metadata: dict
    created_at: datetime

    # 🔒 NEW: user optional image flag (ALWAYS False at preview stage)
    user_original_uploaded: bool = False

    status: str = "PREVIEW_ONLY"
