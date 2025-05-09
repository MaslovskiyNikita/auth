from uuid import UUID

from sqlalchemy import ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import Mapped, mapped_column

from src.auth.infrastructure.db.models.base import Base
from src.auth.infrastructure.db.models.permissions import PermissionsDB


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
    permissions: Mapped[list["PermissionsDB"]] = ForeignKey(
        "permissions", ondelete="CASCADE"
    )

    def __repr__(self):
        return f"<RoleDB(id={self.id}, name={self.name})>"
