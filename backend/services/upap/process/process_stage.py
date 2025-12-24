# UTF-8, English only

class ProcessStage:
    """
    Contract-only process stage (v1).
    No AI, no OCR, no lookup.
    """

    name = "process"

    def run(self, context: dict) -> dict:
        return {
            "status": "ok",
            "stage": "process",
            "record_id": context.get("record_id"),
            "candidates": [],
            "archive_match": False,
            "next": "archive",
        }
