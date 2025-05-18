import uuid

from src.auth.application.exeptions.permission_exeptions import PermissionNotExistsErorr
from src.auth.application.exeptions.role_exeptions import RoleAlreadyExistsErorr
from src.auth.application.repositories.roles_repo.roles_repository import (
    RolesRepositoryABC,
)
from src.auth.application.repositories.uow.uow import UnitOfWorkABC
from src.auth.domain.entity.user_role import Role
from src.auth.presentation.api.rest.v1.schemas.user_role import RoleSchema


class CreateRoleUseCase:
    def __init__(
        self,
        uow: UnitOfWorkABC,
    ):
        self._uow = uow

    async def __call__(self, role: RoleSchema) -> RoleSchema:
        async with self._uow as uow:
            exists_role = await uow.role_repository.exists(role)

            for permission in role.permissions_id:
                exists_permission = await uow.role_repository.exists_permission(
                    permission
                )
                if not exists_permission:
                    raise PermissionNotExistsErorr

            if exists_role:
                raise RoleAlreadyExistsErorr

            await uow.role_repository.save(role)

        return role
