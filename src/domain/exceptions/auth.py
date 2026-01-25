"""Authentication domain exception."""

from src.domain.exceptions.base import DomainException


class InvalidCredentialError(DomainException):
    """Raised when login credentials are invalid."""

    def __init__(self, message: str = "Invalid email or password") -> None:
        super().__init__(message)


class TokenError(DomainException):
    """Raised when token operations fail."""

    def __init__(self, message: str = "Invalid or expired token") -> None:
        super().__init__(message)
