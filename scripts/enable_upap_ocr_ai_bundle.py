"""
UPAP OCR + AI BUNDLE SCRIPT
- Single source of truth
- No external lookup
- No public record view
"""

from pathlib import Path
import textwrap

BASE = Path(__file__).resolve().parents[1]

ENGINE = BASE / "backend/services/upap/engine/upap_engine.py"
OCR_STAGE = BASE / "backend/services/upap/ocr/ocr_stage.py"
AI_STAGE = BASE / "backend/services/upap/ai/ai_stage.py"

ENGINE.parent.mkdir(parents=True, exist_ok=True)
OCR_STAGE.parent.mkdir(parents=True, exist_ok=True)
AI_STAGE.parent.mkdir(parents=True, exist_ok=True)

# ---------------- OCR STAGE ----------------
OCR_STAGE.write_text(textwrap.dedent("""
class OCRStage:
    name = "ocr"

    def run(self, context: dict) -> dict:
        # Placeholder OCR (no external lookup)
        context["ocr_text"] = "[OCR simulated text]"
        context["ocr_status"] = "done"
        print("[UPAP] OCRStage executed")
        return context
""").strip(), encoding="utf-8")

# ---------------- AI STAGE ----------------
AI_STAGE.write_text(textwrap.dedent("""
class AIAnalysisStage:
    name = "ai"

    def run(self, context: dict) -> dict:
        # Placeholder AI analysis (no external calls)
        context["ai_summary"] = "AI analysis placeholder"
        context["ai_status"] = "done"
        print("[UPAP] AIAnalysisStage executed")
        return context
""").strip(), encoding="utf-8")

# ---------------- ENGINE ----------------
ENGINE.write_text(textwrap.dedent("""
import os

from backend.services.upap.archive.archive_stage import ArchiveStage
from backend.services.upap.publish.publish_stage import PublishStage

UPAP_ENABLE_OCR = os.getenv("UPAP_ENABLE_OCR", "false").lower() == "true"
UPAP_ENABLE_AI = os.getenv("UPAP_ENABLE_AI", "false").lower() == "true"

class UPAPEngine:
    def __init__(self):
        self.stages = {}

        self.register_stage(ArchiveStage())
        self.register_stage(PublishStage())

        if UPAP_ENABLE_OCR:
            from backend.services.upap.ocr.ocr_stage import OCRStage
            self.register_stage(OCRStage())

        if UPAP_ENABLE_AI:
            from backend.services.upap.ai.ai_stage import AIAnalysisStage
            self.register_stage(AIAnalysisStage())

    def register_stage(self, stage):
        if not hasattr(stage, "name"):
            raise RuntimeError("Stage must define .name")
        self.stages[stage.name] = stage

    def run_stage(self, name: str, context: dict) -> dict:
        if name not in self.stages:
            raise RuntimeError(f"Stage not registered: {name}")
        return self.stages[name].run(context)

    def run_archive(self, record_id: str):
        context = {"record_id": record_id}
        return self.run_stage("archive", context)

    def run_publish(self, record_id: str):
        context = {"record_id": record_id}
        return self.run_stage("publish", context)

# SINGLETON
upap_engine = UPAPEngine()

# HARD KILLS (NON-NEGOTIABLE)
EXTERNAL_LOOKUP_ENABLED = False
PUBLIC_RECORD_VIEW_ENABLED = False
""").strip(), encoding="utf-8")

print("=== UPAP OCR + AI BUNDLE APPLIED ===")
print("✓ OCR stage")
print("✓ AI stage")
print("✓ Engine rebuilt")
print("✓ External lookup DISABLED")
print("✓ Public record view DISABLED")
print("Next:")
print("1) Restart uvicorn")
print("2) Set ENV flags:")
print("   UPAP_ENABLE_OCR=true")
print("   UPAP_ENABLE_AI=true")
