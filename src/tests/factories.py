import factory
from async_factory_boy.factory.sqlalchemy import AsyncSQLAlchemyFactory

from src.auth.infrastructure.db.models.user import UserDB


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
