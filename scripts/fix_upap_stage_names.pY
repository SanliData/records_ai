"""
FIX UPAP STAGE .name ATTRIBUTES
- Ensures all UPAP stages define .name
- Idempotent
"""

from pathlib import Path
import re

BASE = Path(__file__).resolve().parents[1]

STAGES = {
    "backend/services/upap/archive/archive_stage.py": "archivestage",
    "backend/services/upap/publish/publish_stage.py": "publishstage",
    "backend/services/upap/ocr/ocr_stage.py": "ocrstage",
    "backend/services/upap/ai/ai_stage.py": "aistage",
}

def patch_stage(path: Path, stage_name: str):
    if not path.exists():
        return f"SKIP (missing): {path.name}"

    text = path.read_text(encoding="utf-8")

    # already has name
    if re.search(r"^\s*name\s*=", text, re.MULTILINE):
        return f"OK (already set): {path.name}"

    # find class definition
    m = re.search(r"class\s+(\w+)\s*\(.*?\):", text)
    if not m:
        return f"FAIL (no class): {path.name}"

    cls = m.group(1)

    insert = f"class {cls}"
    replacement = f"class {cls}:\n    name = \"{stage_name}\""

    new_text = text.replace(insert, replacement, 1)
    path.write_text(new_text, encoding="utf-8")

    return f"PATCHED: {path.name} → name='{stage_name}'"


print("=== FIX UPAP STAGE NAMES ===")

for rel, name in STAGES.items():
    result = patch_stage(BASE / rel, name)
    print("•", result)

print("=== DONE ===")
print("Next:")
print("1) Restart uvicorn")
print("2) upload → archive → publish")
