from abc import ABC, abstractmethod

from src.auth.domain.entity.user import User


class UserRepositoryABC(ABC):

    @abstractmethod
    async def save(self, user: User) -> User: ...

    @abstractmethod
    async def check_user_exists(self, email: str) -> bool: ...
