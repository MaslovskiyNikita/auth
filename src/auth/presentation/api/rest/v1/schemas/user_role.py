from uuid import UUID

from pydantic import BaseModel

from src.auth.presentation.api.rest.v1.schemas.permissions import PermissionsSchema


class RolePydantic(BaseModel):
    id: UUID
    permissions: PermissionsSchema
    name: str
