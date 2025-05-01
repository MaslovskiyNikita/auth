from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.application.repositories.user_repository import UserRepositoryABC
from src.auth.infrastructure.db.database import async_session_maker
from src.auth.infrastructure.repositories.user_repository_impl import (
    CreateUserRepository,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


def get_user_repository(session: AsyncSession = Depends(get_db)) -> UserRepositoryABC:
    return CreateUserRepository(session)  # type: ignore [no-untyped-call]
