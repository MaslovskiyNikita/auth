# mypy: disable-error-code="attr-defined,no-untyped-call"
import datetime
import uuid

from src.auth.application.exeptions.user_exeptions import UserAlreadyExistsError
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
from src.auth.presentation.api.rest.v1.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
)


class CreateUserUseCase:
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

    async def __call__(self, user_data: UserCreateSchema) -> UserResponseSchema:
        async with self._uow as uow:
            existing_user = await uow.user_repository.exists(user_data.email)  # type: ignore[*]

            if existing_user:
                raise UserAlreadyExistsError(user_data.email)

            password_hash = self._hashing.hash(str(user_data.password))

            new_user = User(
                id=str(uuid.uuid4()),  # type: ignore[arg-type]
                email=user_data.email,  # type: ignore[arg-type]
                username=user_data.username,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                password=str(password_hash),
                created_at=datetime.datetime.now(),
                updated_at=datetime.datetime.now(),
                roles=[],
                is_active=False,
            )

            saved_user = await uow.user_repository.save(new_user)  # type: ignore[misc]
            await uow.commit()  # type: ignore[no-untyped-call]

            token = self._token_service.generate_token(user_data.email)
            await self._email_service.send_confirmation_email(user_data.email, token)

            return UserResponseSchema(
                id=saved_user.id,
                email=saved_user.email,
                username=saved_user.username,
                first_name=saved_user.first_name,
                last_name=saved_user.last_name,
            )
