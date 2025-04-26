from dataclasses import dataclass
from datetime import datetime
from typing import List

from user_role import Role
from value_objects.user_email import Email
from value_objects.user_id import UserId


@dataclass
class User:

    id: UserId
    email: Email
    username: str
    first_name: str
    last_name: str
    password: str
    created_at: datetime
    updated_at: datetime
    roles: List[Role]
    is_active: bool = True

    def __str__(self):

        return f"User (id={self.id}, email={self.email}, username={self.username}, is_active={self.is_active})"
