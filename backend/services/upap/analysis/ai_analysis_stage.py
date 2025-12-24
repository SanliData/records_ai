
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
