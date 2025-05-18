from abc import ABC, abstractmethod
from contextlib import AbstractAsyncContextManager

from src.auth.application.repositories.roles_repo.roles_repository import (
    RolesRepositoryABC,
)
from src.auth.application.repositories.user_repo.user_repository import (
    UserRepositoryABC,
)


class UnitOfWorkABC(AbstractAsyncContextManager, ABC):

    @abstractmethod
    def user_repository(self) -> "UserRepositoryABC": ...  # type: ignore[misc]

    @abstractmethod
    def role_repository(self) -> "RolesRepositoryABC": ...  # type: ignore[misc]

    @abstractmethod
    async def commit(self): ...

    @abstractmethod
    async def rollback(self): ...
