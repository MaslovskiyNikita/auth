from sqlalchemy import UUID
from sqlalchemy import delete as destroy
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.auth.application.repositories.roles_repo.roles_repository import (
    RolesRepositoryABC,
)
from src.auth.domain.entity.user_role import Role
from src.auth.infrastructure.db.models.permissions import (
    PermissionsDB,
    RolePermissionsAssociation,
)
from src.auth.infrastructure.db.models.user_role import RoleDB


class SQLAlchemyRoleRepository(RolesRepositoryABC):

    def __init__(self, session: AsyncSession):
        self.session = session

    async def exists(self, role: str) -> bool:
        query = select(RoleDB).where(RoleDB.name == role.name)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def exists_permission(self, permission_id: UUID) -> bool:
        query = select(PermissionsDB).where(PermissionsDB.id == permission_id)
        result = await self.session.execute(query)
        return result.scalar_one_or_none() is not None

    async def save(self, role: Role) -> RoleDB:
        orm_role = RoleDB(name=role.name)

        self.session.add(orm_role)
        await self.session.flush()

        for permission_id in role.permissions_id:
            association = RolePermissionsAssociation(
                role_id=orm_role.id, permission_id=permission_id
            )
            self.session.add(association)

        return orm_role

    async def add(self, role: Role) -> None:
        return self.session.add(role)

    async def get(self, role_name: Role) -> RoleDB:
        result = await self.session.execute(
            select(RoleDB)
            .where(RoleDB.name == role_name)
            .options(selectinload(RoleDB.permissions))
        )
        orm_role = result.scalar_one_or_none()
        return orm_role

    async def get_all(self):
        result = await self.session.execute(
            select(RoleDB).options(selectinload(RoleDB.permissions))
        )
        roles = result.scalars().all()
        return roles

    async def update(self, role_name: str, **kwargs) -> RoleDB:  # type: ignore[override]
        stmt = (
            update(RoleDB)
            .where(RoleDB.name == role_name)
            .values(**kwargs)
            .returning(RoleDB)
        )
        result = await self.session.execute(stmt)
        updated_role = result.scalar_one()
        return updated_role

    async def delete(self, role_name) -> None:
        query = destroy(RoleDB).where(RoleDB.name == role_name)
        await self.session.execute(query)
