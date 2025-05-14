from typing import TYPE_CHECKING
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.infrastructure.db.models.base import Base

if TYPE_CHECKING:
    from src.auth.infrastructure.db.models.user_role import RoleDB


class PermissionsDB(Base):
    __tablename__ = "permissions"
    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(unique=True)
    description: Mapped[str] = mapped_column()

    roles: Mapped[list["RoleDB"]] = relationship(
        "RoleDB", secondary="role_permissions", back_populates="permissions"
    )


class RolePermissionsAssociation(Base):
    __tablename__ = "role_permissions"

    role_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )
    permission_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("permissions.id", ondelete="CASCADE"),
        primary_key=True,
    )
