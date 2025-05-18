from abc import ABC, abstractmethod

from src.auth.domain.entity.user import User


class UserRepositoryABC(ABC):

    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def exists(self, email: str) -> bool: ...

    @abstractmethod
    async def get_by_email(self, email: str) -> User | None: ...

    @abstractmethod
    async def get_by_email_password(self, email: str) -> str: ...

    @abstractmethod
    async def add(self, user: User) -> None: ...

    @abstractmethod
    async def delete(self, username: str) -> None: ...
