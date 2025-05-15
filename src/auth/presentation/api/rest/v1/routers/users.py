from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from src.auth.application.use_cases.login_use_case import LoginUserUseCase
from src.auth.application.use_cases.refresh_jwt_tokens import RefreshJWTTokensUseCase
from src.auth.application.use_cases.user_use_case import CreateUserUseCase
from src.auth.application.use_cases.validate_token import ValidateTokenUseCase
from src.auth.main.dependencies.container import Container
from src.auth.presentation.api.rest.v1.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
)

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", response_model=UserResponseSchema)  # type: ignore[misc]
@inject  # type: ignore[misc]
async def create_user(
    user_data: UserCreateSchema,
    use_case: CreateUserUseCase = Depends(Provide[Container.user_use_case]),
) -> UserResponseSchema:
    return await use_case(user_data)


@router.get("/confirm-email")  # type: ignore[misc]
@inject  # type: ignore[misc]
async def confirm_email(
    token: str,
    use_case: ValidateTokenUseCase = Depends(
        Provide[Container.validate_token_use_case]
    ),
):
    await use_case.execute(token=token)
    return {"message": "Email successfully confirmed"}


@router.post("/login")  # type: ignore[misc]
@inject  # type: ignore[misc]
async def login(
    email: str,
    password: str,
    use_case: LoginUserUseCase = Depends(Provide[Container.login_user_use_case]),
):
    tokens = await use_case(email=email, password=password)
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
    }


@router.post("/refresh")  # type: ignore[misc]
@inject  # type: ignore[misc]
async def refresh(
    token: str,
    use_case: RefreshJWTTokensUseCase = Depends(Provide[Container.login_user_use_case]),
):
    tokens = await use_case(token)
    return {
        "access_token": tokens.access_token,
        "refresh_token": tokens.refresh_token,
    }
