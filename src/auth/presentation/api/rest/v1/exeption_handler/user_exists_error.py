from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.auth.application.exeptions.exeptions import UserAlreadyExistsError


def init_exeptions_handlers(app: FastAPI):

    @app.exception_handler(UserAlreadyExistsError)  # type: ignore [misc]
    async def handle_user_already_exists(
        request, exc: UserAlreadyExistsError
    ) -> JSONResponse:
        return JSONResponse(
            status_code=400,
            content={
                "message": str(exc),
                "error_code": "user_already_exists",
                "email": exc.email,
            },
        )
