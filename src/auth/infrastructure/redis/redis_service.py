from redis.asyncio import Redis  # type: ignore[import-untyped]

from src.auth.application.repositories.redis.redis import RedisServiceABC


class RedisService(RedisServiceABC):
    def __init__(self, redis: Redis):
        self._redis = redis

    async def add_to_blacklist(self, jwt: str, expire: int) -> None:
        await self._redis.setex(jwt, time=expire, value="1")

    async def is_blacklisted(self, jwt: str) -> bool:
        return await self._redis.exists(jwt) == 1
