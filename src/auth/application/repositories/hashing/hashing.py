from abc import ABC, abstractmethod


class PasswordHasherABC(ABC):
    @abstractmethod
    def hash(self, password: str) -> str: ...
