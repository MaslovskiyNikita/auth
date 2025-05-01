from datetime import datetime
from typing import List
from uuid import UUID

from pydantic import BaseModel, field_validator

from src.auth.presentation.api.schemas.types import EmailPydantic
from src.auth.presentation.api.schemas.user_role import RolePydantic


class UserModel(BaseModel):
    id: UUID
    email: EmailPydantic
    username: str
    first_name: str
    last_name: str
    password: str
    created_at: datetime
    updated_at: datetime
    roles: List[RolePydantic]
    is_active: bool = True

    class Config:
        from_attributes = True
