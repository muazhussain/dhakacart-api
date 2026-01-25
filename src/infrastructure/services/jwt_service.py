"""JWT tokekn service implementation."""

from datetime import UTC, datetime, timedelta
from uuid import UUID

from jose import JWTError, jwt

from src.application.interfaces.token_service import ITokenService
from src.core.config import settings
from src.domain.exceptions.auth import TokenError


class JWTService(ITokenService):
    """JWT implementation of token service."""

    def __init__(self) -> None:
        self._secret_key = settings.secret_key
        self._algorithm = settings.algorithm
        self._access_token_expire = timedelta(minutes=settings.access_token_expire_minutes)
        self._refresh_token_expire = timedelta(days=settings.refresh_token_expire_days)

    def create_access_token(self, user_id: UUID, role: str) -> str:
        expire = datetime.now(UTC) + self._access_token_expire
        payload = {
            "sub": str(user_id),
            "role": role,
            "type": "access",
            "exp": expire,
            "iat": datetime.now(UTC),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def create_refresh_token(self, user_id: UUID) -> str:
        expire = datetime.now(UTC) + self._refresh_token_expire
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": expire,
            "iat": datetime.now(UTC),
        }
        return jwt.encode(payload, self._secret_key, algorithm=self._algorithm)

    def verify_access_token(self, token: str) -> dict:
        payload = self._decode_token(token)
        if payload.get("type") != "access":
            raise TokenError("Invalid token type")
        return payload

    def verify_refresh_token(self, token: str) -> dict:
        payload = self._decode_token(token)
        if payload.get("type") != "refresh":
            raise TokenError("Invalid token type")
        return payload

    def _decond_token(self, token: str) -> dict:
        try:
            payload = jwt.decode(token, self._secret_key, algorithms=[self._algorithm])
            return payload
        except JWTError as e:
            raise TokenError(f"Token validation failed: {str(e)}") from e
