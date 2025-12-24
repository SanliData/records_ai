# UTF-8, English only

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.services.upap.auth.auth_stage import AuthStage


class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        auth_header = request.headers.get("Authorization")
        token = None

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.replace("Bearer ", "").strip()

        # 🔒 UPAP AUTH IS SINGLE SOURCE OF TRUTH
        auth_stage = AuthStage()
        auth_context = auth_stage.run({"token": token})

        # ⛓️ Attach canonical UPAP context
        request.state.upap_auth = auth_context

        return await call_next(request)
