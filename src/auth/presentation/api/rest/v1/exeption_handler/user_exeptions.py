from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.auth.application.exeptions.exeptions import (
    InvalidPasswordError,
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotActiveError,
    UserNotFoundError,
)


class ExceptionResponseService:
    @classmethod
    def JSONResponse(cls, status_code: int, exc: Exception, error_code: str):
        return JSONResponse(
            status_code=status_code,
            content={
                "message": str(exc),
                "error_code": error_code,
            },
        )


def init_exeptions_handlers(app: FastAPI):
    @app.exception_handler(UserAlreadyExistsError)  # type: ignore[misc]
    async def handle_user_already_exists(
        request, exc: UserAlreadyExistsError
    ) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=400, exc=exc, error_code="user_already_exists"
        )

    @app.exception_handler(UserNotFoundError)  # type: ignore[misc]
    async def handle_user_not_found(request, exc: UserNotFoundError) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=404, exc=exc, error_code="user_not_found"
        )

    @app.exception_handler(InvalidTokenError)  # type: ignore[misc]
    async def handle_invalid_token(request, exc: InvalidTokenError) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=401, exc=exc, error_code="invalid_token"
        )

    @app.exception_handler(UserNotActiveError)  # type: ignore[misc, syntax]
    async def handle_not_activ_user(request, exc: UserNotActiveError) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=400, exc=exc, error_code="not verifyed email"
        )

    @app.exception_handler(InvalidPasswordError)  # type: ignore[misc]
    async def handle_invalid_password(
        request, exc: InvalidPasswordError
    ) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=401, exc=exc, error_code="Invalid password"
        )
