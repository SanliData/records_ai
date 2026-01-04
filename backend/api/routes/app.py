from fastapi import APIRouter, UploadFile, File
from uuid import uuid4

router = APIRouter()

@router.post("/upload")
async def app_upload(
    image: UploadFile = File(...),
    title: str | None = None,
    artist: str | None = None,
    email: str | None = None,
):
    record_id = str(uuid4())

    return {
        "record_id": record_id,
        "status": "PENDING",
        "message": "Upload received. Processing started."
    }


@router.get("/status/{record_id}")
def app_status(record_id: str):
    return {
        "record_id": record_id,
        "stage": "ANALYZING",
        "progress": 0.5,
        "result": None
    }
