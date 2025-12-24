# UTF-8, English only

from fastapi import APIRouter

router = APIRouter(
    prefix="/dashboard",
    tags=["dashboard"],
)


@router.get("")
def dashboard():
    return {
        "service": "records_ai_v2",
        "mode": "UPAP Canonical MVP",
        "version": "2.1.0",
    }
