"""User domain entity."""

from datetime import UTC, datetime
from enum import Enum
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field, field_validator


class Role(str, Enum):
    """User authorization roles."""

    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"


class User(BaseModel):
    """User entity representing a system user."""

    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    hashed_password: str = Field(min_length=1, max_length=255)
    full_name: str = Field(default=None, max_length=20)
    phone: str | None = Field(default=None, max_length=20)
    role: Role = Field(default=Role.CUSTOMER)
    is_active: bool = Field(default=True)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=UTC)
    updated_at: datetime = Field(default_factory=UTC)

    model_config = {
        "frozen": False,
        "validate_assignment": True,
    }

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        """Validate phone number format."""
        if v is None:
            return v

        cleaned = v.replace(" ", "").replace("-", "")
        digits_only = cleaned.replace("+", "")

        if not digits_only.isdigit:
            raise ValueError("Phone must contain only digits and optional + prefix")

        if not 10 <= len(digits_only) <= 15:
            raise ValueError("Phone must be 10-15 digits")

        return v

    def is_admin(self) -> bool:
        """Check if user has admin priviledges."""
        return self.role == Role.ADMIN

    def can_login(self) -> bool:
        """Check if user is allowed to authenticate."""
        return self.is_active

    def update_password(self, new_hashed_password: str) -> None:
        """Update user password hash."""
        if not new_hashed_password:
            raise ValueError("Password cannot be empty.")

        self.hashed_password = new_hashed_password
        self.updated_at = UTC

    def verify_email(self) -> None:
        """Mark email as verified."""
        self.is_verified = True
        self.updated_at = UTC

    def deactivate(self) -> None:
        """Deactivate user account."""
        if self.is_active:
            self.is_active = False
            self.updated_at = UTC

    def activate(self) -> None:
        """Activate user account."""
        if not self.is_active:
            self.is_active = True
            self.updated_at = UTC
