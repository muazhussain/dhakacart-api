"""User registration use case."""

from src.application.dto.requests.user_request import RegisterUserRequest
from src.application.dto.responses.user_response import UserResponse
from src.core.security import hash_password
from src.domain.entities.user import Role, User
from src.domain.exceptions.user import UserAlreadyExistsError
from src.domain.repositories.user_repository import IUserRepository


class RegisterUser:
    """Use case for registering a new user."""

    def __init__(self, user_repository: IUserRepository):
        """Initialize with repository dependency."""
        self.user_repository = user_repository

    async def execute(self, request: RegisterUserRequest) -> UserResponse:
        """
        Register a new user.

        Steps:
        1. check if user already exists
        2. Hash the password
        3. Create domain entity
        4. Save via repository
        5. Return DTO response
        """
        # Check if email already exists
        existing_user = await self.user_repository.get_by_email(request.email)
        if existing_user:
            raise UserAlreadyExistsError(f"User with email {request.email} already exists.")

        # Hash password
        hashed_password = hash_password(request.password)

        # Create domain entity
        user = User(
            email=request.email,
            hashed_password=hashed_password,
            full_name=request.full_name,
            phone=request.phone,
            role=Role.CUSTOMER,
            is_active=True,
        )

        # Persist to database
        created_user = await self.user_repository.create(user)

        # Convert to response DTO
        return UserResponse.model_validate(created_user)
