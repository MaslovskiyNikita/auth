from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse

from src.auth.application.exeptions.permission_exeptions import PermissionNotExistsErorr
from src.auth.application.exeptions.role_exeptions import (
    RoleAlreadyExistsErorr,
    RoleNotExistsError,
)
from src.auth.application.exeptions.user_exeptions import (
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

    @app.exception_handler(RoleAlreadyExistsErorr)  # type: ignore[misc]
    async def handle_existing_role_error(
        request, exc: RoleAlreadyExistsErorr
    ) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=409, exc=exc, error_code="Role alredy exists"
        )

    @app.exception_handler(PermissionNotExistsErorr)  # type: ignore[misc]
    async def handle_not_existing_permission(
        request, exc: PermissionNotExistsErorr
    ) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=404, exc=exc, error_code="Permission not exists"
        )

    @app.exception_handler(RoleNotExistsError)  # type: ignore[misc]
    async def handle_not_existing_role(requst, exc: RoleNotExistsError) -> JSONResponse:
        return ExceptionResponseService.JSONResponse(
            status_code=404, exc=exc, error_code="Role not exists"
        )
