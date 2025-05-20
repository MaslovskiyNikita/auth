from src.auth.application.exeptions.user_exeptions import (
    InvalidPasswordError,
    UserNotFoundError,
)
from src.auth.application.repositories.verificatation.verification_token import (
    TokenServiceABC,
)
from src.auth.infrastructure.db.uow.uow import UnitOfWorkABC
from src.auth.infrastructure.hashing.hashing import PasswordHasherABC


class DeleteUserUseCase:
    def __init__(self, uow: UnitOfWorkABC, token_service: TokenServiceABC):
        self._uow = uow
        self._token_service = token_service

    async def __call__(self, token: str):

        username = self._token_service.decode_jwt_token(token).username

        async with self._uow as uow:
            user = await uow.user_repository.get_by_username(username)

            await uow.user_repository.delete(user.id)
