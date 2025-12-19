from backend.services.upap.archive.archive_stage import ArchiveStage
from backend.services.upap.publish.publish_stage import PublishStage
import os


class UPAPEngine:
    def __init__(self):
        self.stages = {}

        # ZORUNLU ÇEKİRDEK
        self.register_stage(ArchiveStage())
        self.register_stage(PublishStage())

        # OPSİYONEL (ENV ile)
        if os.getenv("UPAP_ENABLE_OCR") == "true":
            from backend.services.upap.ocr.ocr_stage import OCRStage
            self.register_stage(OCRStage())

        if os.getenv("UPAP_ENABLE_AI") == "true":
            from backend.services.upap.ai.ai_stage import AIStage
            self.register_stage(AIStage())

    def register_stage(self, stage):
        if not hasattr(stage, "name"):
            raise RuntimeError(f"{stage.__class__.__name__} missing .name")
        self.stages[stage.name] = stage

    def run_stage(self, stage_name: str, context: dict):
        if stage_name not in self.stages:
            raise RuntimeError(f"Stage not registered: {stage_name}")
        return self.stages[stage_name].run(context)

    def run_archive(self, record_id: str):
        return self.run_stage("archivestage", {"record_id": record_id})

    def run_publish(self, record_id: str):
        return self.run_stage("publishstage", {"record_id": record_id})


# SINGLETON
upap_engine = UPAPEngine()
