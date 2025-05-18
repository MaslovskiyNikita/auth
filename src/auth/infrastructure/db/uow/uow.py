from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.auth.application.repositories.roles_repo.roles_repository import (
    RolesRepositoryABC,
)
from src.auth.application.repositories.uow.uow import UnitOfWorkABC
from src.auth.application.repositories.user_repo.user_repository import (
    UserRepositoryABC,
)
from src.auth.infrastructure.repositories.roles_repository_impl import (
    SQLAlchemyRoleRepository,
)
from src.auth.infrastructure.repositories.user_repository_impl import (
    SQLAlchemyUserRepository,
)


class UnitOfWork(UnitOfWorkABC):
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
        self._session: AsyncSession | None = None
        self._user_repository: UserRepositoryABC | None = None
        self._role_repository: RolesRepositoryABC | None = None

    @property
    def session(self) -> AsyncSession:
        if self._session is None:
            raise RuntimeError("Session not initialized. Use async context manager")
        return self._session

    @property
    def user_repository(self) -> UserRepositoryABC:  # type: ignore[override]
        if self._user_repository is None:
            self._user_repository = SQLAlchemyUserRepository(self.session)
        return self._user_repository

    @property
    def role_repository(self) -> RolesRepositoryABC:  # type: ignore[override]
        if self._role_repository is None:
            self._role_repository = SQLAlchemyRoleRepository(self.session)
        return self._role_repository

    async def __aenter__(self):
        self._session = self.session_factory()

        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        try:
            if exc_type is not None:
                await self.rollback()
            else:
                await self.commit()
        finally:
            await self._session.close()
            self._session = None
            self._user_repository = None
            self._role_repository = None

    async def commit(self):
        if self._session.is_active:
            await self._session.commit()

    async def rollback(self):
        if self._session.is_active:
            await self._session.rollback()
