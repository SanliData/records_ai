# UTF-8, English only

class ArchiveStage:
    """
    Archive commit stage.
    Requires verified user context.
    """

    name = "archive"

    def run(self, context: dict) -> dict:
        user = context.get("user_context")
        if not user or not user.get("email_verified"):
            raise PermissionError("Email verification required")

        record_id = context["record_id"]

        return {
            "status": "ok",
            "stage": "archive",
            "record_id": record_id,
            "user_id": user.get("user_id"),
        }
