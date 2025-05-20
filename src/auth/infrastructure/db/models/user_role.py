from __future__ import annotations

from typing import TYPE_CHECKING, List
from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.auth.infrastructure.db.models.base import Base

if TYPE_CHECKING:
    from src.auth.infrastructure.db.models.permissions import PermissionsDB
    from src.auth.infrastructure.db.models.user import UserDB


class UserRoleAssociation(Base):
    __tablename__ = "user_roles"

    user_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        primary_key=True,
    )
    role_id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True),
        ForeignKey("roles.id", ondelete="CASCADE"),
        primary_key=True,
    )


class RoleDB(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    users: Mapped[List["UserDB"]] = relationship(
        "UserDB", secondary="user_roles", back_populates="roles", lazy="raise"
    )

    permissions: Mapped[List["PermissionsDB"]] = relationship(
        "PermissionsDB",
        secondary="role_permissions",
        back_populates="roles",
        lazy="selectin",
    )
