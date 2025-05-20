from abc import abstractmethod

from src.auth.presentation.api.rest.v1.schemas.user_role import RoleSchema


class RoleConverter:

    @abstractmethod
    def orm_roles_to_roles_schemas(roles):
        result = []
        for role in roles:
            pydantic_model_instance = RoleSchema(
                name=role.name,
                permissions_id=[str(perm.id) for perm in role.permissions],
            )
            result.append(pydantic_model_instance)
        return result
