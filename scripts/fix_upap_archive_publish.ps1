Write-Host "Next step: restart uvicorn and test upload -> archive -> publish
Write-Host "== UPAP Archive + Publish FIX START =="

$base = "backend/services/upap"

# ---------------------------
# archive_store.py
# ---------------------------
$archiveStore = @'
from pathlib import Path
import json
from datetime import datetime, timezone

ARCHIVE_DIR = Path("storage/archive")
ARCHIVE_DIR.mkdir(parents=True, exist_ok=True)


class ArchiveStore:
    def __init__(self):
        self.base_dir = ARCHIVE_DIR

    def _path(self, record_id: str) -> Path:
        return self.base_dir / f"{record_id}.json"

    def is_archived(self, record_id: str) -> bool:
        return self._path(record_id).exists()

    def save(self, record_id: str, payload: dict) -> dict:
        data = {
            "record_id": record_id,
            "archived_at": datetime.now(timezone.utc).isoformat(),
            "payload": payload,
        }
        self._path(record_id).write_text(
            json.dumps(data, indent=2),
            encoding="utf-8"
        )
        return data

    def load(self, record_id: str) -> dict | None:
        path = self._path(record_id)
        if not path.exists():
            return None
        return json.loads(path.read_text(encoding="utf-8"))
'@

Set-Content `
  -Path "$base/archive/archive_store.py" `
  -Value $archiveStore `
  -Encoding UTF8

Write-Host "✓ archive_store.py written"


# ---------------------------
# archive_stage.py
# ---------------------------
$archiveStage = @'
from backend.services.upap.archive.archive_store import ArchiveStore


class ArchiveStage:
    name = "archive"

    def __init__(self):
        self.store = ArchiveStore()

    def run(self, context: dict) -> dict:
        record_id = context.get("record_id")
        if not record_id:
            raise ValueError("record_id is required")

        if self.store.is_archived(record_id):
            return {
                "status": "already_archived",
                "record_id": record_id,
            }

        saved = self.store.save(record_id, context)

        return {
            "status": "archived",
            "record_id": record_id,
            "archive": saved,
        }
'@

Set-Content `
  -Path "$base/archive/archive_stage.py" `
  -Value $archiveStage `
  -Encoding UTF8

Write-Host "✓ archive_stage.py written"


# ---------------------------
# publish_stage.py
# ---------------------------
$publishStage = @'
from backend.services.upap.archive.archive_store import ArchiveStore


class PublishStage:
    name = "publish"

    def __init__(self):
        self.archive = ArchiveStore()

    def run(self, context: dict) -> dict:
        record_id = context.get("record_id")
        if not record_id:
            raise ValueError("record_id is required")

        if not self.archive.is_archived(record_id):
            raise RuntimeError("Record must be archived before publish")

        return {
            "status": "published",
            "record_id": record_id,
        }
'@

Set-Content `
  -Path "$base/publish/publish_stage.py" `
  -Value $publishStage `
  -Encoding UTF8

Write-Host "✓ publish_stage.py written"

Write-Host "== FIX COMPLETE =="
Write-Host "Next step: restart uvicorn and test upload -> archive -> publish"
