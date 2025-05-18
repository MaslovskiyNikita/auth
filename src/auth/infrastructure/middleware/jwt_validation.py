import jwt
from fastapi import Request

from src.auth.application.dto.user import UserDataDTO
from src.auth.application.exeptions.user_exeptions import (
    InvalidTokenError,
    UserNotLogged,
)
from src.auth.infrastructure.middleware.middleware_manager import middleware_manager
from src.auth.main.settings.settings import settings

PUBLIC_PATHS = {
    "/users/login",
    "/users",
    "/docs",
    "/openapi.json",
    "/users/confirm-email",
}


async def jwt_middleware(request: Request, call_next):
    if request.url.path in PUBLIC_PATHS:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header:
        raise UserNotLogged

    access_token = (
        auth_header.split(" ")[1] if auth_header.startswith("Bearer ") else auth_header
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

    return await call_next(request)


middleware_manager.add_middleware(jwt_middleware)
