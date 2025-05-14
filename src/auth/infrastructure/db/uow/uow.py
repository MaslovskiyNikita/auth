from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.auth.application.repositories.uow.uow import UnitOfWorkABC
from src.auth.application.repositories.user_repo.user_repository import (
    UserRepositoryABC,
)
from src.auth.infrastructure.repositories.user_repository_impl import (
    SQLAlchemyUserRepository,
)


class UnitOfWork(UnitOfWorkABC):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None
        self._user_repository: UserRepositoryABC | None = None

    def user_repository(self) -> UserRepositoryABC:
        if self._user_repository is None:
            self._user_repository = SQLAlchemyUserRepository(self.session)
        return self._user_repository

    async def __aenter__(self):
        self.session = self.session_factory()
        self.user_repository = SQLAlchemyUserRepository(self.session)
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type:
            await self.rollback()
        await self.session.close()

    async def commit(self):
        await self.session.commit()

    async def rollback(self):
        await self.session.rollback()
