from abc import ABC, abstractmethod
from datetime import timedelta
from typing import Any


class TokenServiceABC(ABC):
    @abstractmethod
    def generate_token(self, data: Any) -> str: ...

    @abstractmethod
    def validate_token(self, token: str) -> str: ...

    @abstractmethod
    def create_jwt_token(self, data: str, expires: int) -> str: ...

    @abstractmethod
    def decode_jwt_token(self, token: str) -> str: ...
