import datetime
import uuid

from src.auth.application.exeptions.exeptions import UserAlreadyExistsError
from src.auth.application.repositories.user_repository import UserRepositoryABC
from src.auth.domain.entity.user import User
from src.auth.infrastructure.db.uow.uow import UnitOfWork
from src.auth.main.hashing.hashing import hashed_password
from src.auth.presentation.api.rest.v1.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
)


class CreateUserUseCase:
    def __init__(self, uow: UnitOfWork):
        self._uow = uow

    async def __call__(self, user_data: UserCreateSchema) -> UserResponseSchema:
        async with self._uow:
            existing_user = await self._uow.user_repository.check_user_exists(
                user_data.email
            )

            if existing_user:
                await self._uow.rollback()  # type: ignore[no-untyped-call]
                raise UserAlreadyExistsError(user_data.email)

            password_hash = hashed_password(str(user_data.password))

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
                is_active=True,
            )

            saved_user = await self._uow.user_repository.save(new_user)
            await self._uow.commit()  # type: ignore[no-untyped-call]

            return UserResponseSchema(
                id=saved_user.id,
                email=saved_user.email,
                username=saved_user.username,
                first_name=saved_user.first_name,
                last_name=saved_user.last_name,
            )
