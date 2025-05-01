from uuid import UUID

from pydantic import BaseModel

from src.auth.presentation.api.schemas.permissions import Permissions


class RolePydantic(BaseModel):
    id: UUID
    permissions: Permissions
    name: str
