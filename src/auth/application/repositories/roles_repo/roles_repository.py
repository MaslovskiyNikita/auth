from abc import ABC, abstractmethod
from uuid import UUID

from src.auth.domain.entity.user_role import Role


class RolesRepositoryABC(ABC):

    @abstractmethod
    async def save(self, role: Role) -> Role: ...

    @abstractmethod
    async def exists(self, role: str) -> bool: ...

    @abstractmethod
    async def add(self, role: Role) -> None: ...

    @abstractmethod
    async def get(self, role_name: Role) -> Role: ...

    @abstractmethod
    async def get_all(self) -> Role: ...

    @abstractmethod
    async def update(self, role_name, new_data) -> Role: ...

    @abstractmethod
    async def delete(self, role_name: str) -> None: ...
