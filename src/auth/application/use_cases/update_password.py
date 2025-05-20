# mypy: disable-error-code="attr-defined,no-untyped-call"
import datetime
import uuid

from src.auth.application.dto.user import AuthorizationDataDTO
from src.auth.application.exeptions.user_exeptions import UserAlreadyExistsError
from src.auth.application.repositories.hashing.hashing import PasswordHasherABC
from src.auth.application.repositories.uow.uow import UnitOfWorkABC
from src.auth.application.repositories.verificatation.verificate_email import (
    EmailServiceABC,
)
from src.auth.application.repositories.verificatation.verification_token import (
    TokenServiceABC,
)
from src.auth.presentation.api.rest.v1.schemas.user import UserResponseSchema


class DropUserPasswordUseCase:
    def __init__(
        self,
        uow: UnitOfWorkABC,
        hashing: PasswordHasherABC,
        email_service: EmailServiceABC,
        token_service: TokenServiceABC,
    ):
        self._uow = uow
        self._hashing = hashing
        self._email_service = email_service
        self._token_service = token_service

    async def __call__(self, email: str, new_password: str) -> None:
        async with self._uow as uow:
            existing_user = await uow.user_repository.exists(email)  # type: ignore[*]
            if existing_user:
                raise UserAlreadyExistsError(email)
            password_hash = self._hashing.hash(str(new_password))
            data = AuthorizationDataDTO(email=email, password=password_hash)
            token = self._token_service.generate_token(data)
            await self._email_service.send_confirmation_email(email, token)


class NewUserPasswordUseCase:
    def __init__(self, uow: UnitOfWorkABC, token_service: TokenServiceABC):
        self._uow = uow
        self._token_service = token_service

    async def __call__(self, token) -> None:

        async with self._uow as uow:
            user_data = self._token_service.validate_token(token)
            uow.user_repository.update(
                user_data.email, {"password": str(user_data.password)}
            )
