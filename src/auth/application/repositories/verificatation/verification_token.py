from abc import ABC, abstractmethod


class TokenServiceABC(ABC):
    @abstractmethod
    def generate_token(self, data: str) -> str: ...

    @abstractmethod
    def validate_token(self, token: str) -> str: ...
