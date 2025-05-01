from dataclasses import dataclass
from datetime import datetime
from typing import List
from uuid import UUID


@dataclass(frozen=True)
class UserId:
    user_id: UUID
