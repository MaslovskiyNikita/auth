from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.auth.application.use_cases.user_use_case import CreateUserUseCase
from src.auth.infrastructure.db.uow.uow import UnitOfWork
from src.auth.infrastructure.hashing.hashing import PasswordHasher
from src.auth.infrastructure.repositories.user_repository_impl import UserRepository
from src.auth.main.settings.settings import settings


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        packages=["src.auth.presentation.api.rest.v1.routers.users"],
    )

    config = providers.Configuration()

    engine = providers.Singleton(create_async_engine, settings.db_url, echo=True)

    session_factory = providers.Factory(
        async_sessionmaker, bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    user_repository = providers.Factory(
        UserRepository,
        session_factory=session_factory,
    )

    uow = providers.Factory(
        UnitOfWork,
        session_factory=session_factory,
    )

    password_hasher = providers.Factory(PasswordHasher)

    user_use_case = providers.Factory(
        CreateUserUseCase, uow=uow, hashing=password_hasher
    )


container = Container()
