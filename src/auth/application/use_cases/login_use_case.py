import datetime
import uuid

from src.auth.application.dto.token_pair import TokenPair
from src.auth.application.exeptions.exeptions import (
    InvalidPasswordError,
    UserNotActiveError,
    UserNotFoundError,
)
from src.auth.application.repositories.hashing.hashing import PasswordHasherABC
from src.auth.application.repositories.uow.uow import UnitOfWorkABC
from src.auth.application.repositories.user_repo.user_repository import (
    UserRepositoryABC,
)
from src.auth.application.repositories.verificatation.verificate_email import (
    EmailServiceABC,
)
from src.auth.application.repositories.verificatation.verification_token import (
    TokenServiceABC,
)
from src.auth.domain.entity.user import User
from src.auth.main.settings.settings import settings
from src.auth.presentation.api.rest.v1.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
)


class LoginUserUseCase:
    def __init__(
        self,
        uow: UnitOfWorkABC,
        token_service: TokenServiceABC,
        hashing: PasswordHasherABC,
    ):
        self._uow = uow
        self._token_service = token_service
        self._hashing = hashing

    async def __call__(self, email: str, password: str) -> TokenPair:
        async with self._uow as uow:
            existing_user = await uow.user_repository.get_by_email(email)  # type: ignore[*]

            if not existing_user:
                raise UserNotFoundError(email)

            # Проверка на то, активировал ли пользователь свою почту или нет
            if not existing_user.is_active:
                raise UserNotActiveError()

            user_password = existing_user.password
            hashed_password = self._hashing.hash(password=password)

            if user_password != hashed_password:
                raise InvalidPasswordError()

            access_token = self._token_service.create_jwt_token(
                data=existing_user,
                expires=settings.jwt_config.access_token_expire,
            )

            refresh_token = self._token_service.create_jwt_token(
                data=existing_user,
                expires=settings.jwt_config.refresh_token_expire,
            )

            token_pair = TokenPair(access_token, refresh_token)

            return token_pair
