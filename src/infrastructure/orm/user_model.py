"""User ORM model for database persistence."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from src.infrastructure.orm.base import Base, TimestampMixin, uuidpk


class UserModel(Base, TimestampMixin):
    """
    User table model.

    Maps to 'users' table in PostgreSQL.
    Inherits created_at/updated_at from TimestampMixin.
    """

    __tablename__ = "users"

    id: Mapped[uuidpk]
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    phone: Mapped[str | None] = mapped_column(String(20), nullable=True)
    role: Mapped[str] = mapped_column(String(20), nullable=False, default="CUSTOMER", index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_verified: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)

    def __repr__(self) -> str:
        """String representation for debugging."""
        return f"<UserModel(id={self.id}, email={self.email}, role={self.role})>"
