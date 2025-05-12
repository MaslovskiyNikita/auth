import asyncio

import pytest
from dependency_injector import providers
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.auth.infrastructure.db.models.base import Base
from src.auth.infrastructure.db.uow.uow import UnitOfWork
from src.auth.main.dependencies.container import container
from src.auth.main.main import app
from src.auth.main.settings.settings import settings

TEST_DATABASE_URL = settings.test_db_url


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
async def uow(session):
    return UnitOfWork(session_factory=lambda: session)


@pytest.fixture
async def async_client(uow):

    container.uow.override(providers.Factory(lambda: uow))

    async with AsyncClient(
        base_url="http://testserver"
        # "http://127.0.0.1:8000"
    ) as client:
        yield client


@pytest.fixture(autouse=True)
async def cleanup(session):
    yield
    await session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
    await session.commit()
