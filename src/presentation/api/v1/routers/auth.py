"""Authentication API router."""

from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.requests.auth_request import LoginRequest
from src.application.dto.requests.user_request import RegisterUserRequest
from src.application.dto.responses.auth_response import TokenResponse
from src.application.dto.responses.user_response import UserResponse
from src.application.use_cases.user.login_user import LoginUser
from src.application.use_cases.user.register_user import RegisterUser
from src.domain.exceptions.auth import InvalidCredentialError
from src.domain.exceptions.user import UserAlreadyExistsError
from src.infrastructure.database.session import get_session
from src.infrastructure.repositories.sqlalchemy.user_repository_impl import (
    SQLAlchemyUserRepository,
)
from src.infrastructure.services.jwt_service import JWTService

router = APIRouter(prefix="/auth", tags=["Authentication"])


def get_user_repository(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SQLAlchemyUserRepository:
    return SQLAlchemyUserRepository(session)


def get_register_use_case(
    user_repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
) -> RegisterUser:
    return RegisterUser(user_repository)


def get_login_use_case(
    user_repository: Annotated[SQLAlchemyUserRepository, Depends(get_user_repository)],
) -> LoginUser:
    token_service = JWTService()
    return LoginUser(user_repository, token_service)


@router.post(
    "/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account.",
)
async def register(
    request: RegisterUserRequest,
    use_case: Annotated[RegisterUser, Depends(get_register_use_case)],
) -> UserResponse:
    try:
        return await use_case.execute(request)
    except UserAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        ) from None


@router.post(
    "/login",
    response_model=TokenResponse,
    status_code=status.HTTP_200_OK,
    summary="User login",
    description="Authenticate user and return access/refresh tokens.",
)
async def login(
    request: LoginRequest,
    use_case: Annotated[LoginUser, Depends(get_login_use_case)],
) -> TokenResponse:
    try:
        return await use_case.execute(request)
    except InvalidCredentialError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=e.message,
            headers={"WWW-Authenticate": "Bearer"},
        ) from None
