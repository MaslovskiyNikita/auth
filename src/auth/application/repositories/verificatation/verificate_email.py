from abc import ABC, abstractmethod
from typing import Any, Dict


class EmailServiceABC(ABC):
    @abstractmethod
    async def send_confirmation_email(self, to_email: str, token: str) -> None: ...
