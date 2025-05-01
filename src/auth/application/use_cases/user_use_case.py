from src.auth.application.repositories.user_repository import UserRepositoryABC
from src.auth.domain.entity.user import User


class CreateUserUseCase:
    def __init__(self, user_repository: UserRepositoryABC):
        self._user_repository = user_repository

    async def _check_user_exists(self, email):
        # Временная заглушка:
        return False

    async def __call__(self, user):

        existing_user = await self._check_user_exists(user.email)

        if existing_user:
            raise f"Такой емайл {user.email} уже существует"

        new_user = User(**user.__dict__)

        return await self._user_repository.save(new_user)
