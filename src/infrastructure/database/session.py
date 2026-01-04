"""Database session management and dependency injection."""

from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.infrastructure.database.connection import engine

# Session factory
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


async def get_session() -> AsyncGenerator[AsyncSession]:
    """
    Dependency that provides database session to FastAPI routes.

    Usage in FastAPI:
        @app.get("/users")
        async def get_users(session: SessionDep):
            result = await session.execute (select(User))
            return result.scalars().all()

    Automatically:
    - Creates session
    - Commits on success
    - Rolls back on execution
    - Closes session
    """
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


# Type alias for dependency injection
SessionDep = Annotated[AsyncSession, Depends(get_session)]
