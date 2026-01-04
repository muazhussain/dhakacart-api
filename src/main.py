from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.core.logging import get_logger, setup_logging
from src.infrastructure.database import engine

# Setup logging
setup_logging()
logger = get_logger(__name__)


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """
    Application lifespan manager.

    Handles startup and shutdown events.
    """
    # Startup
    logger.info(
        "Application starting...",
        extra={
            "app_name": settings.app_name,
            "version": settings.app_version,
            "environment": settings.environment,
            "debug": settings.debug,
        },
    )

    # Database connection info
    db_host = (
        settings.database.url.split("@")[1].split("/")[0]
        if "@" in settings.database.url
        else "unknown"
    )
    logger.info(
        "Database engine initialized",
        extra={
            "host": db_host,
            "pool_size": settings.database.pool_size,
            "max_overflow": settings.database.max_overflow,
        },
    )

    yield

    # Shutdown
    logger.info("Disposing database engine...")
    await engine.dispose()
    logger.info("Application shutdown complete")


# Create app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="Dhakacart API",
    docs_url=f"{settings.api_prefix}/docs",
    redoc_url=f"{settings.api_prefix}/redoc",
    openapi_url=f"{settings.api_prefix}/openapi.json",
    debug=settings.debug,
    lifespan=lifespan,
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Root endpoint
@app.get("/", tags=["Root"])
async def root() -> dict[str, str]:
    """Root endpoint."""
    return {
        "message": "Welcome to Dhakacart",
        "docs": f"{settings.api_prefix}/docs",
        "health": "/health",
    }


# Health check endpoint
@app.get("/health", tags=["Health"])
async def health_check() -> dict[str, str | bool]:
    """Health check endpoint."""
    logger.debug("Health check called")
    return {
        "status": "healthy",
        "app": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
    }
