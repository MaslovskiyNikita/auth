from src.auth.application.dto.token_pair import TokenPair
from src.auth.application.exeptions.exeptions import InvalidTokenError
from src.auth.application.repositories.redis.redis import CashServiceABC
from src.auth.application.repositories.verificatation.verification_token import (
    TokenServiceABC,
)
from src.auth.main.settings.settings import settings


class RefreshJWTTokensUseCase:
    def __init__(self, token_service: TokenServiceABC, redis: CashServiceABC):
        self._token_service = token_service
        self._redis_service = redis

    async def __call__(self, refresh_token: str) -> TokenPair:

        if await self._redis_service.get(refresh_token):  # type: ignore[call-arg]
            raise InvalidTokenError("Token revoked")

        try:
            payload = self._token_service.decode_jwt_token(refresh_token)
        except:
            raise InvalidTokenError

        new_access_token = self._token_service.create_jwt_token(
            data=payload, expires=settings.jwt_config.access_token_expire
        )
        new_refresh_token = self._token_service.create_jwt_token(
            data=payload, expires=settings.jwt_config.refresh_token_expire
        )

        await self._redis_service.add(
            jwt=refresh_token, expire=int(payload["exp"])  # type: ignore[index]
        )

        return TokenPair(access_token=new_access_token, refresh_token=new_refresh_token)
