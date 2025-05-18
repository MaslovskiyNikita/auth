from typing import List

from pydantic import UUID4, BaseModel

from src.auth.presentation.api.rest.v1.schemas.permissions import PermissionsSchema


class RoleSchema(BaseModel):
    name: str
    permissions_id: List[UUID4]
