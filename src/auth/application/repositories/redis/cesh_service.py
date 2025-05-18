from abc import ABC, abstractmethod


class CeshServiceABC(ABC):
    @abstractmethod
    async def add(self, jwt: str, expire: int) -> None:
        pass

    @abstractmethod
    async def get(self, jwt: str) -> bool:
        pass
