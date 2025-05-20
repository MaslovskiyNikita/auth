from uuid import UUID

from pydantic import BaseModel


class PermissionsSchema(BaseModel):
    name: str
