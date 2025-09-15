from dataclasses import dataclass
from typing import List
from uuid import UUID

from src.auth.domain.value_objects.permissions import PermissionPool


@dataclass
class Permissions:
    id: UUID
    name: str
