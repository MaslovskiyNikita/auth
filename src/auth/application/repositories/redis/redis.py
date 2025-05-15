from abc import ABC, abstractmethod


class RedisServiceABC(ABC):
    @abstractmethod
    async def add_to_blacklist(self, jwt: str, expire: int) -> None:
        pass

    @abstractmethod
    async def is_blacklisted(self, jwt: str) -> bool:
        pass
