from src.auth.application.exeptions.role_exeptions import RoleNotExistsError
from src.auth.application.repositories.uow.uow import UnitOfWorkABC


class UpdateRoleUseCase:
    def __init__(
        self,
        uow: UnitOfWorkABC,
    ):
        self._uow = uow

    async def __call__(self, role_name, **kwargs) -> None:
        async with self._uow as uow:
            exists_role = await uow.role_repository.get(role_name)

            if not exists_role:
                raise RoleNotExistsError

            await uow.role_repository.update(role_name, **kwargs)
            return exists_role
