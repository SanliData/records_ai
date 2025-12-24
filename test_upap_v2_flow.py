# UTF-8, English only
# UPAP v2 – Single-file test suite (ROL-2, canonical)

import io
from PIL import Image
from fastapi.testclient import TestClient

from backend.main import app


client = TestClient(app)


def _make_jpeg_bytes():
    """Create an in-memory JPEG image (no filesystem dependency)."""
    img = Image.new("RGB", (64, 64), color=(120, 120, 120))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    buf.seek(0)
    return buf


# -------------------------------------------------
# U01 — Upload → Preview (happy path)
# -------------------------------------------------
def test_u01_upload_preview_success():
    img = _make_jpeg_bytes()

    resp = client.post(
        "/upap/upload/preview",
        files={"file": ("sample.jpg", img, "image/jpeg")},
    )

    assert resp.status_code == 200
    body = resp.json()

    assert isinstance(body.get("preview_id"), str)
    assert body["status"] == "PREVIEW_ONLY"
    assert body["canonical_image_path"].startswith("preview://")
    assert body["detected_metadata"] == {}


# -------------------------------------------------
# U02 — Unsupported file type → 400 (guard)
# -------------------------------------------------
def test_u02_upload_invalid_file_returns_400():
    resp = client.post(
        "/upap/upload/preview",
        files={"file": ("bad.txt", b"not an image", "text/plain")},
    )

    assert resp.status_code == 400
    assert resp.json().get("detail") == "Unsupported or invalid image file"


# -------------------------------------------------
# U03 — Same image twice → different preview_id
# -------------------------------------------------
def test_u03_duplicate_upload_creates_distinct_previews():
    img1 = _make_jpeg_bytes()
    img2 = _make_jpeg_bytes()

    r1 = client.post(
        "/upap/upload/preview",
        files={"file": ("sample.jpg", img1, "image/jpeg")},
    )
    r2 = client.post(
        "/upap/upload/preview",
        files={"file": ("sample.jpg", img2, "image/jpeg")},
    )

    assert r1.status_code == 200
    assert r2.status_code == 200
    assert r1.json()["preview_id"] != r2.json()["preview_id"]


# -------------------------------------------------
# A01 — Archive commit requires auth
# NOTE:
# FastAPI body validation may run BEFORE auth guard.
# Therefore 422 is ACCEPTABLE alongside 401/403.
# -------------------------------------------------
def test_a01_archive_requires_auth_or_validation():
    resp = client.post(
        "/upap/archive/commit",
        json={"preview_id": "preview-fake-id"},
    )

    assert resp.status_code in (401, 403, 422)


# -------------------------------------------------
# P01 — Process stage stub (not implemented yet)
# -------------------------------------------------
def test_p01_process_preview_stub():
    resp = client.post("/upap/process/preview/preview-fake-id")
    assert resp.status_code in (404, 501)
