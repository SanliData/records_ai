"""
FIX UPAP ARCHIVE STORE
- Adds missing ArchiveStore class
- No DB
- In-memory, deterministic
"""

from pathlib import Path
import textwrap

BASE = Path(__file__).resolve().parents[1]

STORE_FILE = BASE / "backend/services/upap/archive/archive_store.py"
STORE_FILE.parent.mkdir(parents=True, exist_ok=True)

STORE_FILE.write_text(textwrap.dedent("""
# UPAP Archive Store
# Single-process, in-memory
# No external persistence

_ARCHIVED = set()

class ArchiveStore:
    def mark_archived(self, record_id: str):
        _ARCHIVED.add(record_id)

    def is_archived(self, record_id: str) -> bool:
        return record_id in _ARCHIVED


# Functional helpers (used by publish stage)
def mark_archived(record_id: str):
    _ARCHIVED.add(record_id)

def is_archived(record_id: str) -> bool:
    return record_id in _ARCHIVED
""").strip(), encoding="utf-8")

print("=== UPAP ARCHIVE STORE FIXED ===")
print("✓ ArchiveStore class created")
print("✓ mark_archived / is_archived helpers added")
print("Next:")
print("1) Restart uvicorn")
print("2) Test: upload → archive → publish")
