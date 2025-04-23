import uuid
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional
from uuid import UUID


@dataclass
class Role:

    id: UUID
    permissions: List[str] = field(default_factory=list)
    name: str = ""

    def __str__(self):
        return f"Role(id={self.id}, name={self.name}, permissions={self.permissions})"


@dataclass
class User:

    id: UUID
    email: str = ""
    username: str = ""
    first_name: str = ""
    last_name: str = ""
    password: str = ""
    is_active: bool = True
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)
    roles: List[Role] = field(default_factory=list)

    def __str__(self):

        return f"User (id={self.id}, email={self.email}, username={self.username}, is_active={self.is_active})"


@dataclass
class UserRole:

    user_id: UUID
    role_id: UUID

    def __str__(self):

        return f"User Role(user_id={self.user_id}, role_id={self.role_id})"
