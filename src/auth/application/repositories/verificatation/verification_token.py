from abc import ABC, abstractmethod
from datetime import timedelta


class TokenServiceABC(ABC):
    @abstractmethod
    def generate_token(self, data: str) -> str: ...

    @abstractmethod
    def validate_token(self, token: str) -> str: ...

    @abstractmethod
    def create_jwt_token(self, data: str, expires: int) -> str: ...

    @abstractmethod
    def decode_jwt_token(self, token: str) -> str: ...
