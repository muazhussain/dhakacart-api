"""Base ORM models and mixins."""

from datetime import datetime
from typing import Annotated
from uuid import UUID, uuid4

from sqlalchemy import DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

# Type annotations for common column types
intpk = Annotated[int, mapped_column(primary_key=True)]
uuidpk = Annotated[UUID, mapped_column(primary_key=True, default=uuid4)]
timestamp = Annotated[
    datetime,
    mapped_column(DateTime(timezone=True), server_default=func.now()),
]
timestamp_updated = Annotated[
    datetime,
    mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    ),
]


class Base(DeclarativeBase):
    """
    Base class for all ORM models.

    All database models inherit from this.
    Provides metadata for table creation and Alembic migrations.
    """

    pass


class TimestampMixin:
    """
    Mixin that adds timestamp fields to models.

    Adds:
    - created_at: Auto-set when row is created
    - updated_at: Auto-updated when row is modified

    Usage:
        Class User(Base, TimestampMixin):
            __tablename__ = "users"
            id: Mapped[intpk]
            email: Mapped[str]
            # created_at and updated_at auto-added
    """

    created_at: Mapped[timestamp]
    updated_at: Mapped[timestamp_updated]
