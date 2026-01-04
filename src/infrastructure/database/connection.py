"""Database connection and engine configuration."""

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine

from src.core.config import settings

# Create async engine with connection pooling
engine: AsyncEngine = create_async_engine(
    settings.database.url,
    echo=settings.database.echo,
    pool_size=settings.database.pool_size,
    max_overflow=settings.database.max_overflow,
    pool_pre_ping=True,
    future=True,
)
