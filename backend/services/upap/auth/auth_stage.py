# UTF-8, English only

from backend.storage.user_store import get_user_by_token


class AuthStage:
    """
    Auth stage.
    Preview is allowed without authentication.
    """

    name = "auth"

    def run(self, payload: dict) -> dict:
        token = payload.get("token")

        if not token:
            return {
                "scope": "preview",
                "email_verified": False,
            }

        user = get_user_by_token(token)
        if not user:
            return {
                "scope": "preview",
                "email_verified": False,
            }

        return {
            "user_id": user["id"],
            "email": user["email"],
            "email_verified": user["email_verified"],
            "scope": "user",
        }
