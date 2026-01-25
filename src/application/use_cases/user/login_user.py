"""User login use case."""

from src.application.dto.requests.auth_request import LoginRequest
from src.application.dto.responses.auth_response import TokenResponse
from src.application.interfaces.token_service import ITokenService
from src.core.security import verify_password
from src.domain.exceptions.auth import InvalidCredentialError
from src.domain.repositories.user_repository import IUserRepository


class LoginUser:
    """Use case for authenticating a user and issuing tokens."""

    def __init__(
        self,
        user_repository: IUserRepository,
        token_service: ITokenService,
    ) -> None:
        self._user_repository = user_repository
        self._token_service = token_service

    async def execute(self, request: LoginRequest) -> TokenResponse:
        user = await self._user_repository.get_by_email(request.email)
        if not user:
            raise InvalidCredentialError()

        if not verify_password(request.password, user.hashed_password):
            raise InvalidCredentialError()

        if not user.is_active:
            raise InvalidCredentialError("Account is deactivated")

        access_token = self._token_service.create_access_token(user.id, user.role)
        refresh_token = self._token_service.create_refresh_token(user.id)

        return TokenResponse(
            access_token=access_token,
            refresh_token=refresh_token,
        )
