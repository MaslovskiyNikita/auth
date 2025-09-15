from uuid import UUID

from sqlalchemy.orm import Mapped, mapped_column

from src.auth.infrastructure.db.models.base import Base


class PermissionsDB(Base):
    __tablename__ = "permissions"
    id: Mapped[UUID] = mapped_column(primary_key=True, unique=True)
    name: Mapped[str] = mapped_column()
    description: Mapped[str] = mapped_column()
