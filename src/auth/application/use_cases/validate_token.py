from fastapi import HTTPException

from src.auth.application.exeptions.exeptions import (
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
        except Exception as e:
            raise InvalidTokenError("Invalid or expired token") from e

        async with self._uow:
            user_db = await self._uow.user_repository.get_by_email(email)  # type: ignore[attr-defined]
            if not user_db:
                raise UserNotFoundError("User not found")

            user_db.is_active = True
            self._uow.session.add(user_db)  # type: ignore[attr-defined, no-untyped-call]

            await self._uow.commit()  # type: ignore[no-untyped-call]
