# UTF-8, English only

from fastapi import APIRouter, Form
from backend.services.upap.engine.upap_engine import get_upap_engine

router = APIRouter(
    prefix="/upap/process",
    tags=["upap-process"],
)


@router.post("/preview")
def process_preview(record_id: str = Form(...)):
    engine = get_upap_engine()
    return engine.run_stage(
        "process",
        {
            "record_id": record_id,
        },
    )
