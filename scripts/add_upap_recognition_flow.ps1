# ================================
# UPAP Recognition Flow Bootstrap
# ================================
$ErrorActionPreference = "Stop"

Write-Host "== ADDING UPAP RECOGNITION FLOW =="

$apiPath = "backend/api/v1"

# 1) Recognition router
$recognitionPath = "$apiPath/upap_recognition_router.py"
@"
from fastapi import APIRouter
from datetime import datetime, timezone
import uuid

router = APIRouter(
    prefix="/upap/recognition",
    tags=["upap-recognition"],
)

@router.post("/candidate")
def recognition_candidate(record_id: str):
    candidate_id = str(uuid.uuid4())
    return {
        "status": "ok",
        "record_id": record_id,
        "candidate_id": candidate_id,
        "source": "placeholder",
        "confidence": 0.65,
        "suggested": {
            "artist": "UNKNOWN",
            "title": "UNKNOWN",
            "label": None,
            "year": None,
        },
        "needs_user_confirmation": True,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
"@ | Set-Content $recognitionPath -Encoding UTF8

Write-Host "✓ upap_recognition_router.py created"

# 2) System archive confirm router
$archivePath = "$apiPath/upap_system_archive_router.py"
@"
from fastapi import APIRouter
from datetime import datetime, timezone

router = APIRouter(
    prefix="/upap/archive/system",
    tags=["upap-archive-system"],
)

@router.post("/confirm")
def system_archive_confirm(candidate_id: str, approved: bool = True):
    if not approved:
        return {"status": "skipped", "candidate_id": candidate_id}

    return {
        "status": "archived",
        "candidate_id": candidate_id,
        "system_record_id": candidate_id,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }
"@ | Set-Content $archivePath -Encoding UTF8

Write-Host "✓ upap_system_archive_router.py created"

# 3) main.py update
$mainPath = "backend/main.py"
$main = Get-Content $mainPath -Raw

if ($main -notmatch "upap_recognition_router") {
    $main = $main -replace "from backend.api.v1.upap_publish_router import router as upap_publish_router",
@"
from backend.api.v1.upap_publish_router import router as upap_publish_router
from backend.api.v1.upap_recognition_router import router as upap_recognition_router
from backend.api.v1.upap_system_archive_router import router as upap_system_archive_router
"@
}

if ($main -notmatch "app.include_router\(upap_recognition_router\)") {
    $main = $main -replace "app.include_router\(upap_publish_router\)",
@"
app.include_router(upap_publish_router)
    app.include_router(upap_recognition_router)
    app.include_router(upap_system_archive_router)
"@
}

$main | Set-Content $mainPath -Encoding UTF8

Write-Host "✓ main.py updated"

Write-Host ""
Write-Host "=== DONE ==="
Write-Host "Endpoints added:"
Write-Host "POST /upap/recognition/candidate"
Write-Host "POST /upap/archive/system/confirm"
Write-Host "Next step: docker build and deploy"
