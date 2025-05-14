from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.exeptions.exeptions import (
    InvalidTokenError,
    UserNotFoundError,
)
from src.auth.application.repositories.user_repo.user_repository import (
    UserRepositoryABC,
)
from src.auth.application.use_cases.login_use_case import LoginUserUseCase
from src.auth.application.use_cases.user_use_case import CreateUserUseCase
from src.auth.application.use_cases.validate_token import ValidateTokenUseCase
from src.auth.domain.entity.user import User
from src.auth.infrastructure.db.uow.uow import UnitOfWork
from src.auth.infrastructure.repositories.user_repository_impl import (
    SQLAlchemyUserRepository,
)
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
    response: Response = None,
):
    tokens = await use_case(email=email, password=password)
    response.headers["X-Access-Token"] = tokens.access_token
    response.headers["X-Refresh-Token"] = tokens.refresh_token
    return {"message": "Login successful"}
