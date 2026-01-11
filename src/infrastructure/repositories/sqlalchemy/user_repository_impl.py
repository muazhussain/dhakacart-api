"""SQLAlchemy implementation of User repository."""

from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entities.user import User
from src.domain.repositories.user_repository import IUserRepository
from src.infrastructure.orm.user_model import UserModel


class SQLAlchemyUserRepository(IUserRepository):
    """SQLAlchemy-based User repository implementation."""

    def __init__(self, session: AsyncSession) -> None:
        """
        Initialize repository with database session.

        Args:
            session: SQLAlchemy async database session
        """
        self._session = session

    async def create(self, user: User) -> User:
        """Create new user."""
        db_user = self._to_orm(user)
        self._session.add(db_user)

        try:
            await self._session.flush()
            await self._session.refresh(db_user)
        except IntegrityError as e:
            await self._session.rollback()
            raise ValueError(f"User with email {user.email} already exists") from e

        return self._to_entity(db_user)

    async def get_by_id(self, user_id: UUID) -> User | None:
        """Get user by ID."""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        db_user = result.scalar_one_or_none()

        return self._to_entity(db_user) if db_user else None

    async def get_by_email(self, email: str) -> User | None:
        """Get user by email."""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)
        db_user = result.scalar_one_or_none()

        return self._to_entity(db_user) if db_user else None

    async def update(self, user: User) -> User:
        """Update existing user."""
        stmt = select(UserModel).where(UserModel.id == user.id)
        result = await self._session.execute(stmt)
        db_user = result.scalar_one_or_none()

        if not db_user:
            raise ValueError(f"User with id {user.id} not found!")

        # Update fields
        db_user.email = user.email
        db_user.hashed_password = user.hashed_password
        db_user.full_name = user.full_name
        db_user.phone = user.phone
        db_user.role = user.role.value
        db_user.is_active = user.is_active
        db_user.is_verified = user.is_verified
        db_user.updated_at = user.updated_at

        await self._session.flush()
        await self._session.refresh(db_user)

        return self._to_entity(db_user)

    async def delete(self, user_id: UUID) -> bool:
        """Delete user by ID."""
        stmt = select(UserModel).where(UserModel.id == user_id)
        result = await self._session.execute(stmt)
        db_user = result.scalar_one_or_none()

        if not db_user:
            return False

        await self._session.delete(db_user)
        await self._session.flush()

        return True

    async def exists_by_email(self, email: str) -> bool:
        """Check if user exists by email."""
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self._session.execute(stmt)

        return result.scalar_one_or_none() is not None

    def _to_entity(self, db_user: UserModel) -> User:
        """
        Convert ORM model to domain entity.

        Args:
            db_user: SQLAlchemy UserModel instance

        Returns:
            Domain User entity
        """
        return User(
            id=db_user.id,
            email=db_user.email,
            hashed_password=db_user.hashed_password,
            full_name=db_user.full_name,
            phone=db_user.phone,
            role=db_user.role,
            is_active=db_user.is_active,
            is_verified=db_user.is_verified,
            created_at=db_user.created_at,
            updated_at=db_user.updated_at,
        )

    def _to_orm(self, user: User) -> UserModel:
        """
        Converts domain entity to ORM model.

        Args:
            user: Domain User entity

        Returns:
            SQLAlchemy UserModel instance
        """
        return UserModel(
            id=user.id,
            email=user.email,
            hashed_password=user.hashed_password,
            full_name=user.full_name,
            phone=user.phone,
            role=user.role.value,
            is_active=user.is_active,
            is_verified=user.is_verified,
            created_at=user.created_at,
            updated_at=user.updated_at,
        )
