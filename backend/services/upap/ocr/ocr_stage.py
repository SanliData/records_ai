class OCRStage:
    name = "ocr"

    def run(self, context: dict) -> dict:
        # Placeholder OCR (no external lookup)
        context["ocr_text"] = "[OCR simulated text]"
        context["ocr_status"] = "done"
        print("[UPAP] OCRStage executed")
        return context