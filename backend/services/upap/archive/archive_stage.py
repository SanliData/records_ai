from backend.services.upap.archive.archive_store import mark_archived


class ArchiveStage:
    name = "archivestage"

    def run(self, context: dict):
        record_id = context["record_id"]
        mark_archived(record_id)
        return {
            "status": "ok",
            "stage": "archive",
            "record_id": record_id
        }
