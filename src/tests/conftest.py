import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.auth.infrastructure.db.models.base import Base
from src.auth.infrastructure.db.models.permissions import PermissionsDB
from src.auth.infrastructure.db.models.user import UserDB
from src.auth.infrastructure.db.uow.uow import UnitOfWork
from src.auth.infrastructure.repositories.token_use_case import ItsDangerousTokenService
from src.auth.main.dependencies.container import container
from src.auth.main.main import app
from src.auth.main.settings.settings import settings
from src.tests.factories import ActiveUserFactory

TEST_DATABASE_URL = settings.db_settings.test_db_url


@pytest.fixture(scope="session", autouse=True)
async def setup_db():
    engine = create_async_engine(TEST_DATABASE_URL)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)

    await engine.dispose()


@pytest.fixture
async def engine():
    return create_async_engine(TEST_DATABASE_URL, echo=True)


@pytest.fixture
async def session_factory(engine):
    return async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture
async def session(session_factory):
    async with session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()


@pytest.fixture
async def uow(session: AsyncSession):
    return UnitOfWork(session_factory=lambda: session)


@pytest.fixture
async def async_client(uow):

    container.uow.override(providers.Factory(lambda: uow))

    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://127.0.0.1:8000"
    ) as client:
        yield client


@pytest.fixture(autouse=True)
async def cleanup(session):
    yield
    await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    tables = ["users", "roles", "permissions", "user_roles", "role_permissions"]
    await session.execute(
        text(f"TRUNCATE TABLE {','.join(tables)} RESTART IDENTITY CASCADE")
    )
    await session.commit()


@pytest.fixture
def token_service():
    return ItsDangerousTokenService(settings)


@pytest.fixture
async def test_user(session: AsyncSession):
    user_data = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "is_active": True,
    }

    user = await ActiveUserFactory.create_async(session=session, **user_data)
    yield user
    await session.delete(user)
    await session.commit()


@pytest.fixture
def auth_token(test_user: UserDB, token_service: ItsDangerousTokenService):
    payload = {
        "user_id": str(test_user.id),
        "email": test_user.email,
        "username": test_user.username,
        "first_name": test_user.first_name,
        "last_name": test_user.last_name,
        "roles": test_user.roles,
        "exp": int,
    }
    return token_service.create_jwt_token(
        data=payload, expires=settings.jwt_config.access_token_expire
    )


@pytest.fixture
async def auth_client(async_client: AsyncClient, auth_token: str):
    async_client.headers.update({"Authorization": f"Bearer {auth_token}"})
    return async_client


@pytest.fixture
async def auth_headers(auth_token: str):
    return {"Authorization": f"Bearer {auth_token}"}


@pytest.fixture
async def setup_permissions(session):
    permissions = [
        {"name": "create", "description": "a"},
        {"name": "read", "description": "a"},
        {"name": "update", "description": "b"},
        {"name": "delete", "description": "c"},
    ]
    for perm in permissions:
        permission = PermissionsDB(**perm)
        session.add(permission)
    await session.commit()
