from uuid import UUID

from pydantic import BaseModel


class Permissions(BaseModel):
    id: UUID
    name: str
