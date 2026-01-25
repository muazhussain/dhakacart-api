"""Token service interface."""

from abc import ABC, abstractmethod
from uuid import UUID


class ITokenService(ABC):
    """Abstract interface for token operations."""

    @abstractmethod
    def create_access_token(self, user_id: UUID, role: str) -> str:
        """Generate an access token for a user."""
        pass

    @abstractmethod
    def create_refresh_token(self, user_id: UUID) -> str:
        """Generate a refresh token for a user."""
        pass

    @abstractmethod
    def verify_access_token(self, token: str) -> dict:
        """Verify and decode an access token. Raises TokenError if invalid."""
        pass

    @abstractmethod
    def verify_refresh_token(self, token: str) -> dict:
        """Verify and decode a refresh token. Raises TokenError if invalid."""
        pass
