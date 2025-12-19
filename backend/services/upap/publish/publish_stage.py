from backend.services.upap.archive.archive_store import is_archived


class PublishStage:
    name = "publishstage"

    def run(self, context: dict):
        record_id = context["record_id"]

        if not is_archived(record_id):
            raise ValueError("Record must be archived before publish")

        return {
            "status": "ok",
            "stage": "publish",
            "record_id": record_id
        }
