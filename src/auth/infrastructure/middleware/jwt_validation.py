import jwt
from fastapi import Request

from auth.main.settings.settings import settings
from src.auth.application.exeptions.exeptions import InvalidTokenError, UserNotLogged
from src.auth.main.main import app

PUBLIC_PATHS = {
    "/users/login",
    "/users",
    "/docs",
    "/openapi.json",
    "/users/confirm-email",
}


@app.middleware("http")  # type: ignore[misc]
async def jwt_middleware(request: Request, call_next):
    if request.url in PUBLIC_PATHS:
        return await call_next(request)

    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise UserNotLogged

    access_token = auth_header.split(" ")[1]

    try:
        jwt.decode(
            access_token,
            settings.token_secret_key,
            algorithm=settings.jwt_config.jwt_hashing,
            options={"verify_exp": True},
        )
    except:
        raise InvalidTokenError

    return await call_next(request)
