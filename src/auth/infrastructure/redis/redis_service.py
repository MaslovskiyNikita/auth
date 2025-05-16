from redis.asyncio import Redis  # type: ignore[import-untyped]

from src.auth.application.repositories.redis.redis import CashServiceABC
from src.auth.main.settings import settings


class RedisService(CashServiceABC):
    def __init__(self):
        self._redis = Redis(
            host=settings.redis_config.host,
            port=settings.redis_config.port,
            db=settings.redis_config.db,
        )

    async def add(self, jwt: str, expire: int) -> None:
        await self._redis.setex(jwt, time=expire, value="1")

    async def get(self, jwt: str) -> bool:
        return await self._redis.exists(jwt) == 1
