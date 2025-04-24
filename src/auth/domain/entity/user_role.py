from dataclasses import dataclass
from typing import List
from uuid import UUID


@dataclass
class Role:
    id: UUID
    permissions: List[str]
    name: str = ""

    def __str__(self):
        return f"Role(id={self.id}, name={self.name}, permissions={self.permissions})"


@dataclass
class UserRole:
    user_id: UUID
    role_id: UUID

    def __str__(self):

        return f"User Role(user_id={self.user_id}, role_id={self.role_id})"
