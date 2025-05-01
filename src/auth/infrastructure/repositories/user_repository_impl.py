from src.auth.application.repositories.user_repository import UserRepositoryABC
from src.auth.domain.entity.user import User
from src.auth.infrastructure.db.models.user import UserDB


class CreateUserRepository(UserRepositoryABC):

    def __init__(self, session):
        self.session = session

    async def save(self, user: User) -> User:
        orm_user = UserDB(**user.__dict__)
        self.session.add(orm_user)
        await self.session.commit()
        await self.session.refresh(orm_user)
        return orm_user
