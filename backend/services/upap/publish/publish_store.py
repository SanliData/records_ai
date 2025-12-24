# -*- coding: utf-8 -*-

import json
from pathlib import Path

BASE_DIR = Path("storage/state")
BASE_DIR.mkdir(parents=True, exist_ok=True)


def _path(record_id: str, mode: str) -> Path:
    return BASE_DIR / f"publish_{record_id}_{mode}.json"


def is_published(record_id: str, mode: str = "public") -> bool:
    return _path(record_id, mode).exists()


def get_publish_metadata(record_id: str, mode: str = "public") -> dict:
    p = _path(record_id, mode)
    if not p.exists():
        return {}
    return json.loads(p.read_text(encoding="utf-8"))


def mark_published(record_id: str, mode: str, metadata: dict) -> None:
    p = _path(record_id, mode)
    p.write_text(json.dumps(metadata, indent=2), encoding="utf-8")
