from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.auth.domain.entity.permission import Permissions


@dataclass
class Role:
    id: UUID
    permissions: Permissions
    name: str

    def __str__(self):
        return f"Role(id={self.id}, name={self.name}, permissions={self.permissions})"
