import jwt
from fastapi import Request
from fastapi.responses import JSONResponse
from jwt import InvalidTokenError

from src.auth.application.exeptions.exeptions import UserNotLogged
from src.auth.infrastructure.dto.user import UserDataDTO
from src.auth.main.settings.settings import settings


def init_middleware(app):

    PUBLIC_PATHS = {
        "/users/login",
        "/users/",
        "/docs/",
        "/openapi.json",
        "/users/confirm-email/",
    }

    @app.middleware("http")  # type: ignore[misc]
    async def jwt_middleware(request: Request, call_next):

        if request.url.path in PUBLIC_PATHS:
            return await call_next(request)

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
                algorithm=[settings.jwt_config.jwt_hashing],
                options={"verify_exp": True},
            )

            user_data = UserDataDTO(
                username=payload["username"],
                first_name=payload["first_name"],
                last_name=payload["last_name"],
                roles=payload["roles"],
                email=payload["email"],
            )

        except:
            raise InvalidTokenError

        request.state.user = user_data

        return await call_next(request)
