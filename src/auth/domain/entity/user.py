# mypy: ignore-errors

from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID

from user_role import Role


@dataclass
class User:

    id: UUID
    email: str
    username: str
    first_name: str
    last_name: str
    password: str
    is_active: bool = True
    created_at: datetime
    updated_at: datetime
    roles: List[Role]

    def __str__(self):

        return f"User (id={self.id}, email={self.email}, username={self.username}, is_active={self.is_active})"
