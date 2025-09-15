from uuid import UUID

from pydantic import BaseModel


class PermissionsSchema(BaseModel):
    id: UUID
    name: str
