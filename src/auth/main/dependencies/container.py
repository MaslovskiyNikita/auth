import aioboto3
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.auth.application.use_cases.user_use_case import CreateUserUseCase
from src.auth.application.use_cases.validate_token import ValidateTokenUseCase
from src.auth.infrastructure.aws.ses_manager import SESEmailService
from src.auth.infrastructure.db.uow.uow import UnitOfWork
from src.auth.infrastructure.hashing.hashing import HashlibPasswordHasher
from src.auth.infrastructure.repositories.token_use_case import ItsDangerousTokenService
from src.auth.infrastructure.repositories.user_repository_impl import (
    SQLAlchemyUserRepository,
)
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
        SQLAlchemyUserRepository,
        session_factory=session_factory,
    )

    uow = providers.Factory(
        UnitOfWork,
        session_factory=session_factory,
    )

    password_hasher = providers.Factory(HashlibPasswordHasher)

    session_aioboto3 = providers.Singleton(
        aioboto3.Session,
        aws_access_key_id=settings.aws_ses_access_key_id,
        aws_secret_access_key=settings.aws_ses_secret_access_key,
        region_name=settings.region,
    )

    email_service = providers.Factory(
        SESEmailService,
        session=session_aioboto3,
        endpoint_url=settings.aws_ses_endpoint_url,
        source_email=settings.email_host_user,
    )

    token_service = providers.Factory(
        ItsDangerousTokenService,
        secret_key=settings.token_secret_key,
        salt=settings.salt,
        max_age=3600,
    )

    user_use_case = providers.Factory(
        CreateUserUseCase,
        uow=uow,
        hashing=password_hasher,
        email_service=email_service,
        token_service=token_service,
    )

    validate_token_use_case = providers.Factory(
        ValidateTokenUseCase, token_service=token_service, uow=uow
    )


container = Container()
