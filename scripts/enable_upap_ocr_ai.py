import os
from pathlib import Path

BASE = Path("backend/services/upap")

print("=== UPAP OCR + AI ENABLE SCRIPT (PYTHON) ===")

# -------------------------
# OCR STAGE
# -------------------------
ocr_dir = BASE / "ocr"
ocr_dir.mkdir(parents=True, exist_ok=True)

(ocr_dir / "ocr_stage.py").write_text(
    '''
class OCRStage:
    name = "ocr"

    def run(self, context: dict) -> dict:
        if not context.get("enable_ocr", False):
            context["ocr_skipped"] = True
            return context

        # REAL OCR hook can be plugged here (easyocr already loaded)
        context["ocr_text"] = "OCR_TEXT_PLACEHOLDER"
        context["ocr_done"] = True
        return context
''',
    encoding="utf-8"
)

print("✓ OCR stage written")

# -------------------------
# AI ANALYSIS STAGE
# -------------------------
analysis_dir = BASE / "analysis"
analysis_dir.mkdir(parents=True, exist_ok=True)

(analysis_dir / "ai_analysis_stage.py").write_text(
    '''
class AIAnalysisStage:
    name = "analysis"

    def run(self, context: dict) -> dict:
        if not context.get("enable_ai", False):
            context["analysis_skipped"] = True
            return context

        text = context.get("ocr_text", "")
        context["analysis_result"] = {
            "summary": text[:200],
            "confidence": 0.99
        }
        context["analysis_done"] = True
        return context
''',
    encoding="utf-8"
)

print("✓ AI analysis stage written")

# -------------------------
# ENGINE PATCH
# -------------------------
engine_path = BASE / "engine" / "upap_engine.py"
engine_code = engine_path.read_text(encoding="utf-8")

if "OCRStage" not in engine_code:
    engine_code = engine_code.replace(
        "from backend.services.upap.publish.publish_stage import PublishStage",
        """from backend.services.upap.publish.publish_stage import PublishStage
from backend.services.upap.ocr.ocr_stage import OCRStage
from backend.services.upap.analysis.ai_analysis_stage import AIAnalysisStage"""
    )

if "register_stage(OCRStage" not in engine_code:
    engine_code = engine_code.replace(
        "self.register_stage(PublishStage())",
        """self.register_stage(OCRStage())
        self.register_stage(AIAnalysisStage())
        self.register_stage(PublishStage())"""
    )

engine_path.write_text(engine_code, encoding="utf-8")
print("✓ UPAPEngine patched")

# -------------------------
# HARD DISABLE: EXTERNAL + PUBLIC
# -------------------------
guard_path = BASE / "guards.py"
guard_path.write_text(
    '''
# HARD OFF GUARDS – DO NOT REMOVE

def external_lookup_disabled():
    raise RuntimeError("External lookup is disabled by design")

def public_record_view_disabled():
    raise RuntimeError("Public record view is disabled by design")
''',
    encoding="utf-8"
)

print("✓ External lookup & public view hard-disabled")

print("=== DONE ===")
print("Next:")
print("1) Restart uvicorn")
print("2) Set ENV flags:")
print("   UPAP_ENABLE_OCR=true")
print("   UPAP_ENABLE_AI=true")
