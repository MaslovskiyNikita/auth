from datetime import datetime
from uuid import UUID

from base import Base
from sqlalchemy import ARRAY, Boolean, DateTime, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from user import UserDB


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

    user: Mapped["UserDB"] = relationship(back_populates="role_associations")
    role: Mapped["RoleDB"] = relationship(back_populates="user_associations")


class RoleDB(Base):
    __tablename__ = "roles"

    id: Mapped[UUID] = mapped_column(
        PG_UUID(as_uuid=True), primary_key=True, server_default=func.gen_random_uuid()
    )
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    permissions: Mapped[list[str]] = mapped_column(ARRAY(String(50)))

    user_associations: Mapped[list["UserRoleAssociation"]] = relationship(
        back_populates="role", cascade="all, delete-orphan", passive_deletes=True
    )

    @property
    def users(self) -> list["UserDB"]:
        return [assoc.user for assoc in self.user_associations]

    def __repr__(self):
        return f"<RoleDB(id={self.id}, name={self.name})>"
