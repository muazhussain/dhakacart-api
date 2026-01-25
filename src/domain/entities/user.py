"""User domain entity."""

from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4


class Role(str, Enum):
    """User authorization roles."""

    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"


@dataclass
class User:
    """User entity representing a system user."""

    email: str
    hashed_password: str
    id: UUID = field(default_factory=uuid4)
    full_name: str | None = None
    phone: str | None = None
    role: Role = Role.CUSTOMER
    is_active: bool = True
    is_verified: bool = False
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    def is_admin(self) -> bool:
        """Check if user has admin privileges."""
        return self.role == Role.ADMIN

    def can_login(self) -> bool:
        """Check if user is allowed to authenticate."""
        return self.is_active
