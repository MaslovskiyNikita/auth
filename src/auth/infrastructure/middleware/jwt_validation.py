import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from jwt import ExpiredSignatureError
from starlette.middleware.base import BaseHTTPMiddleware

from src.auth.application.dto.user import UserDataDTO
from src.auth.application.exeptions.user_exeptions import (
    InvalidTokenError,
    UserNotLogged,
)
from src.auth.main.settings.settings import settings


class JWTAuthMiddleware(BaseHTTPMiddleware):
    PUBLIC_PATHS = {
        "/users/login",
        "/users/",
        "/docs",
        "/openapi.json",
        "/users/confirm-email",
    }

    async def dispatch(self, request: Request, call_next):
        if request.url.path in self.PUBLIC_PATHS:
            return await call_next(request)

        try:
            auth_header = request.headers.get("Authorization")
            if not auth_header:
                raise UserNotLogged

            access_token = (
                auth_header.split(" ")[1]
                if auth_header.startswith("Bearer ")
                else auth_header
            )

            try:
                payload = jwt.decode(
                    access_token,
                    settings.token_secret_key,
                    algorithms=[settings.jwt_config.jwt_hashing],
                    options={"verify_exp": True},
                )
                request.state.user = UserDataDTO(**payload)
            except jwt.InvalidTokenError:
                raise InvalidTokenError
            except jwt.ExpiredSignatureError:
                raise ExpiredSignatureError

            return await call_next(request)

        except UserNotLogged as exc:
            return JSONResponse(status_code=401, content={"detail": str(exc)})
