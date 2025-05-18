from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Body, Depends

from src.auth.application.use_cases.login_use_case import LoginUserUseCase
from src.auth.application.use_cases.refresh_jwt_tokens import RefreshJWTTokensUseCase
from src.auth.application.use_cases.roles.create_role import CreateRoleUseCase
from src.auth.application.use_cases.roles.delete_role import DeleteRoleUseCase
from src.auth.application.use_cases.roles.read_roles import ReadRolesUseCase
from src.auth.application.use_cases.roles.update_role import UpdateRoleUseCase
from src.auth.application.use_cases.user_use_case import CreateUserUseCase
from src.auth.application.use_cases.validate_token import ValidateTokenUseCase
from src.auth.main.dependencies.container import Container
from src.auth.presentation.api.rest.v1.schemas.converter.role_converter import (
    RoleConverter,
)
from src.auth.presentation.api.rest.v1.schemas.user import (
    UserCreateSchema,
    UserResponseSchema,
)
from src.auth.presentation.api.rest.v1.schemas.user_role import RoleSchema

router = APIRouter(prefix="/roles", tags=["Roles"])


@router.post("/create")  # type: ignore[misc]
@inject  # type: ignore[misc]
async def create_role(
    role_data: RoleSchema,
    use_case: CreateRoleUseCase = Depends(Provide[Container.create_role_use_case]),
) -> RoleSchema:
    role_schema = await use_case(role_data)
    return role_schema


@router.delete("/delete")  # type: ignore[misc]
@inject  # type: ignore[misc]
async def delete_role(
    role_name: str,
    use_case: DeleteRoleUseCase = Depends(Provide[Container.delete_role_use_case]),
) -> dict:
    await use_case(role_name)
    return {"Message": "Succesfully"}


@router.get("/read")  # type: ignore[misc]
@inject  # type: ignore[misc]
async def read_roles(
    use_case: ReadRolesUseCase = Depends(Provide[Container.read_roles_use_case]),
) -> List[RoleSchema]:
    result = await use_case()
    roles = RoleConverter.orm_roles_to_roles_schemas(result)  # type: ignore[misc]
    return roles


@router.patch("/update")  # type: ignore[misc]
@inject  # type: ignore[misc]
async def update_role(
    role_name: str,
    update_data: dict,
    use_case: UpdateRoleUseCase = Depends(Provide[Container.update_role_use_case]),
) -> dict:
    await use_case(role_name, **update_data)
    return {"message": f"succesfully updated {role_name}"}
