from typing import Annotated

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.repositories.user_repository import UserRepositoryABC
from src.auth.application.use_cases.user_use_case import CreateUserUseCase
from src.auth.domain.entity.user import User
from src.auth.infrastructure.db.database import Container
from src.auth.infrastructure.db.uow.uow import UnitOfWork
from src.auth.infrastructure.repositories.user_repository_impl import (
    CreateUserRepository,
)
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
