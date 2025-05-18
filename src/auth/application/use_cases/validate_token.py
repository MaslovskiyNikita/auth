from fastapi import HTTPException
from jwt import PyJWTError

from src.auth.application.exeptions.user_exeptions import (
    InvalidTokenError,
    UserNotFoundError,
)
from src.auth.application.repositories.uow.uow import UnitOfWorkABC
from src.auth.application.repositories.verificatation.verification_token import (
    TokenServiceABC,
)


class ValidateTokenUseCase:
    def __init__(self, token_service: TokenServiceABC, uow: UnitOfWorkABC):
        self._token_service = token_service
        self._uow = uow

    async def execute(self, token: str) -> None:
        try:
            email = self._token_service.validate_token(token)
        except:
            raise InvalidTokenError

        async with self._uow as uow:
            user_db = await uow.user_repository.get_by_email(email)  # type: ignore[attr-defined]
            if not user_db:
                raise UserNotFoundError

            user_db.is_active = True
            await uow.user_repository.add(user_db)  # type: ignore[attr-defined, no-untyped-call]
            await uow.commit()
