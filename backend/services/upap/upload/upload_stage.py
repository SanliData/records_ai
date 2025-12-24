# UTF-8, English only

import uuid
from backend.services.upap.engine.stage_interface import StageInterface


class UploadStage(StageInterface):
    """
    Upload stage.
    Canonical JPEG ONLY enters the system.
    """

    name = "upload"

    def validate_input(self, context: dict) -> None:
        """
        Validate input payload for upload stage.

        Requirements:
        - file_bytes must exist and be bytes
        - content_type must be 'image/jpeg'

        This method satisfies the abstract contract
        defined in StageInterface.
        """
        if "file_bytes" not in context:
            raise ValueError("Missing file_bytes in upload context")

        if not isinstance(context["file_bytes"], (bytes, bytearray)):
            raise TypeError("file_bytes must be bytes")

        if context.get("content_type") != "image/jpeg":
            raise ValueError("UploadStage accepts only canonical JPEG")

    def run(self, context: dict) -> dict:
        file_bytes: bytes = context["file_bytes"]
        content_type: str = context["content_type"]

        # Defensive check (already validated, but safe)
        if content_type != "image/jpeg":
            raise ValueError("UploadStage accepts only canonical JPEG")

        record_id = str(uuid.uuid4())

        # Storage is abstracted away (preview store)
        canonical_url = f"preview://{record_id}.jpg"

        return {
            "record_id": record_id,
            "canonical_image_url": canonical_url,
            "size_bytes": len(file_bytes),
        }
