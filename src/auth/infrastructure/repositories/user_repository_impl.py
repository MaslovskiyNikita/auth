from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.auth.application.repositories.user_repository import UserRepositoryABC
from src.auth.domain.entity.user import User
from src.auth.infrastructure.db.models.user import UserDB


class SQLAlchemyUserRepository(UserRepositoryABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, email: str) -> bool:
        query = select(UserDB).where(UserDB.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def save(self, user: User) -> User:
        orm_user = UserDB(**user.__dict__)
        self.session.add(orm_user)
        await self.session.flush()
        return orm_user

    async def get_by_email(self, email: str) -> UserDB | None:
        query = select(UserDB).where(UserDB.email == email)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()
