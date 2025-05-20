import uuid

from src.auth.application.exeptions.permission_exeptions import PermissionNotExistsErorr
from src.auth.application.exeptions.role_exeptions import (
    RoleAlreadyExistsErorr,
    RoleNotExistsError,
)
from src.auth.application.repositories.roles_repo.roles_repository import (
    RolesRepositoryABC,
)
from src.auth.application.repositories.uow.uow import UnitOfWorkABC
from src.auth.domain.entity.user_role import Role
from src.auth.presentation.api.rest.v1.schemas.user_role import RoleSchema


class ReadRolesUseCase:
    def __init__(
        self,
        uow: UnitOfWorkABC,
    ):
        self._uow = uow

    async def __call__(self) -> Role:
        async with self._uow as uow:
            roles = await uow.role_repository.get_all()
            return roles
