from dataclasses import dataclass
from typing import List
from uuid import UUID

from value_objects.permissions import PermissionPool


@dataclass
class Permission:
    id: UUID
    name: str
