# UTF-8, English only
# Records_AI v2.1.0 – UPAP Canonical Engine

from datetime import datetime

from backend.models.preview_record import PreviewRecord
from backend.storage.preview_store import save_preview

from backend.services.upap.auth.auth_stage import AuthStage
from backend.services.upap.upload.upload_stage import UploadStage
from backend.services.upap.process.process_stage import ProcessStage
from backend.services.upap.archive.archive_stage import ArchiveStage
from backend.services.upap.publish.publish_stage import PublishStage


class UPAPEngine:
    """
    Canonical UPAP pipeline engine.
    Single source of truth for stage execution.
    """

    def __init__(self):
        self.stages = {}

        # ORDER IS BINDING
        self.register_stage(AuthStage())
        self.register_stage(UploadStage())
        self.register_stage(ProcessStage())
        self.register_stage(ArchiveStage())
        self.register_stage(PublishStage())

    def register_stage(self, stage):
        if not hasattr(stage, "name"):
            raise RuntimeError(f"{stage.__class__.__name__} missing .name")
        self.stages[stage.name] = stage

    def run_stage(self, stage_name: str, context: dict):
        if stage_name not in self.stages:
            raise RuntimeError(f"Stage not registered: {stage_name}")

        stage = self.stages[stage_name]

        # Stage contract
        stage.validate_input(context)
        result = stage.run(context)

        # Preview persistence is allowed ONLY after upload
        if stage_name == "upload":
            preview = PreviewRecord(
                preview_id=f"preview-{result['record_id']}",
                record_id=result["record_id"],
                canonical_image_path=result["canonical_image_url"],
                detected_metadata={},
                status="PREVIEW_ONLY",
                created_at=datetime.utcnow(),
            )
            save_preview(preview)
            return preview.model_dump()

        return result

    def run_archive(self, record_id: str, user_context: dict):
        return self.run_stage(
            "archive",
            {
                "record_id": record_id,
                "user_context": user_context,
            },
        )

    def run_publish(self, record_id: str, user_context: dict):
        return self.run_stage(
            "publish",
            {
                "record_id": record_id,
                "user_context": user_context,
            },
        )


# Singleton accessor (ONLY allowed entry)
_upap_engine_instance = None


def get_upap_engine() -> UPAPEngine:
    global _upap_engine_instance
    if _upap_engine_instance is None:
        _upap_engine_instance = UPAPEngine()
    return _upap_engine_instance
