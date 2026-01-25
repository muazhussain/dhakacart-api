"""User domain exceptions."""

from src.domain.exceptions.base import DomainException


class UserAlreadyExistsError(DomainException):
    """Raised when attempting to register with existing email."""

    def __init__(self, message: str = "User already exists") -> None:
        super().__init__(message)


class UserNotFoundError(DomainException):
    """Raised when user is not found."""

    def __init__(self, message: str = "User not found") -> None:
        super().__init__(message)
