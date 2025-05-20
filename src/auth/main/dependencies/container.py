import aioboto3
from dependency_injector import containers, providers
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

from src.auth.application.use_cases.delete_user import DeleteUserUseCase
from src.auth.application.use_cases.login_use_case import LoginUserUseCase
from src.auth.application.use_cases.refresh_jwt_tokens import RefreshJWTTokensUseCase
from src.auth.application.use_cases.roles.create_role import CreateRoleUseCase
from src.auth.application.use_cases.roles.delete_role import DeleteRoleUseCase
from src.auth.application.use_cases.roles.read_roles import ReadRolesUseCase
from src.auth.application.use_cases.roles.update_role import UpdateRoleUseCase
from src.auth.application.use_cases.update_password import (
    DropUserPasswordUseCase,
    NewUserPasswordUseCase,
)
from src.auth.application.use_cases.user_use_case import CreateUserUseCase
from src.auth.application.use_cases.validate_token import ValidateTokenUseCase
from src.auth.infrastructure.aws.ses_manager import SESEmailService
from src.auth.infrastructure.db.uow.uow import UnitOfWork
from src.auth.infrastructure.hashing.hashing import HashlibPasswordHasher
from src.auth.infrastructure.redis.redis_service import CeshService
from src.auth.infrastructure.repositories.roles_repository_impl import (
    SQLAlchemyRoleRepository,
)
from src.auth.infrastructure.repositories.token_use_case import ItsDangerousTokenService
from src.auth.infrastructure.repositories.user_repository_impl import (
    SQLAlchemyUserRepository,
)
from src.auth.main.settings.settings import AppSettings


class Container(containers.DeclarativeContainer):

    wiring_config = containers.WiringConfiguration(
        packages=[
            "src.auth.presentation.api.rest.v1.routers.users",
            "src.auth.presentation.api.rest.v1.routers.tokens",
            "src.auth.presentation.api.rest.v1.routers.roles",
        ],
    )

    config = providers.Configuration()

    base_settings = providers.Singleton()

    settings = providers.Singleton(AppSettings)

    engine = providers.Singleton(
        create_async_engine, settings.provided.db_settings.db_url, echo=True
    )

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
        aws_access_key_id=settings.provided.aws_settings.aws_ses_access_key_id,
        aws_secret_access_key=settings.provided.aws_settings.aws_ses_secret_access_key,
        region_name=settings.provided.aws_settings.region,
    )

    email_service = providers.Factory(
        SESEmailService,
        session=session_aioboto3,
        settings=settings,
    )

    token_service = providers.Factory(
        ItsDangerousTokenService,
        settings=settings,
        max_age=3600,
    )

    cesh_repository = providers.Factory(CeshService)

    refresh_jwt_tokens_use_case = providers.Factory(
        RefreshJWTTokensUseCase, redis=cesh_repository, token_service=token_service
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

    login_user_use_case = providers.Factory(
        LoginUserUseCase, uow=uow, token_service=token_service, hashing=password_hasher
    )

    destroy_user_use_case = providers.Factory(
        DeleteUserUseCase, uow=uow, token_service=token_service
    )

    drop_user_password_use_case = providers.Factory(
        DropUserPasswordUseCase,
        uow=uow,
        hashing=password_hasher,
        email_service=email_service,
        token_service=token_service,
    )

    new_user_password_use_case = providers.Factory(
        NewUserPasswordUseCase, uow=uow, token_service=token_service
    )

    roles_service = providers.Factory(SQLAlchemyRoleRepository, session=session_factory)

    create_role_use_case = providers.Factory(CreateRoleUseCase, uow=uow)

    delete_role_use_case = providers.Factory(DeleteRoleUseCase, uow=uow)

    read_roles_use_case = providers.Factory(ReadRolesUseCase, uow=uow)

    update_role_use_case = providers.Factory(UpdateRoleUseCase, uow=uow)


container = Container()
