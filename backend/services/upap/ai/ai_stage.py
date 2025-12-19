class AIAnalysisStage:
    name = "ai"

    def run(self, context: dict) -> dict:
        # Placeholder AI analysis (no external calls)
        context["ai_summary"] = "AI analysis placeholder"
        context["ai_status"] = "done"
        print("[UPAP] AIAnalysisStage executed")
        return context