import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory

from src.auth.infrastructure.db.models.user import UserDB
from src.auth.infrastructure.hashing.hashing import HashlibPasswordHasher


class UserFactory(AsyncSQLAlchemyFactory):
    class Meta:
        model = UserDB
        sqlalchemy_session = None
        sqlalchemy_session_persistence = "flush"

    id = factory.Faker("uuid4")
    email = factory.Faker("email", domain="example.com")
    username = factory.Faker("user_name")
    first_name = factory.Faker("first_name")
    last_name = factory.Faker("last_name")
    password = factory.Faker("password")
    is_active = False

    @classmethod
    async def create_async(cls, session, **kwargs):
        if "password" in kwargs:
            hasher = HashlibPasswordHasher()
            kwargs["password"] = hasher.hash(kwargs["password"])
        user = cls.build(**kwargs)
        session.add(user)
        await session.commit()
        await session.refresh(user)
        return user
