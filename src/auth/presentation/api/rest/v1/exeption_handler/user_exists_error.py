from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.auth.application.exeptions.exeptions import (
    InvalidTokenError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class ExceptionResponseService:

    @classmethod
    def JSONResponse(self, status_code, exc, error_code):
        return JSONResponse(
            status_code=status_code,
            content={
                "message": str(exc),
                "error_code": error_code,
                "email": exc.email,
            },
        )


def init_exeptions_handlers(app: FastAPI):

    @app.exception_handler(UserAlreadyExistsError)  # type: ignore [misc]
    async def handle_user_already_exists(
        request, exc: UserAlreadyExistsError
    ) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=400, exc=exc, error_code="user_already_exists"
        )

    """
    @app.exception_handler(UserNotFoundError)
    async def handle_user_not_found(
        request, exc: UserNotFoundError
    ) -> JSONResponse:
        return"""
