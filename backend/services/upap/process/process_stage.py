from backend.services.upap.process.text_normalizer import TextNormalizer
from backend.services.upap.process.fuzzy_matcher import FuzzyMatcher

class ProcessStage:
    name = "process"

    def validate_input(self, context: dict):
        if "ocr_text" not in context:
            raise ValueError("Missing 'ocr_text' in context")

    def run(self, context: dict) -> dict:
        ocr_text = context.get("ocr_text", "")
        normalized = TextNormalizer.clean(ocr_text)
        candidates = context.get("candidate_titles", [])
        matches = FuzzyMatcher.match(normalized, candidates)
        context["normalized_ocr_text"] = normalized
        context["matches"] = matches
        return context
