"""Logging configuration for Dhakacart API."""

import logging
import sys
from pathlib import Path

from pythonjsonlogger import jsonlogger

from src.core.config import settings


def setup_logging() -> None:
    """
    Configure application logging with JSON formatting.

    Sets up:
    - Console handler (stdout) - human-readable in dev, JSON in prod
    - File handler (logs/app.log) - always JSON format
    - Log level from settings
    """
    # Create logs directory if it doesn't exist
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(settings.log_level)

    # Remove existing handlers to avoid duplicates
    root_logger.handlers.clear()

    # JSON formatter for structured logging
    json_formatter = jsonlogger.JsonFormatter(
        fmt="%(asctime)s %(name)s %(levelname)s %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler - JSON in production, simple in development
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(settings.log_level)

    if settings.is_production:
        # JSON format for production (parseable by log aggregators)
        console_handler.setFormatter(json_formatter)
    else:
        # Human-readable format for development
        console_formatter = logging.Formatter(
            fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
            datefmt="%H:%M:%S",
        )
        console_handler.setFormatter(console_formatter)

    root_logger.addHandler(console_handler)

    # File handler
    file_handler = logging.FileHandler(log_dir / "app.log")
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(json_formatter)
    root_logger.addHandler(file_handler)

    # Suppress overly verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    # Log startup message
    logger = logging.getLogger(__name__)
    logger.info(
        "Logging configured",
        extra={
            "environment": settings.environment,
            "log_level": settings.log_level,
            "app_version": settings.app_version,
        },
    )


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a module.

    Usage:
        logger = get_logger(__name__)
        logger.info("Something happened", extra={"user_id": 123})

    Args:
        name: Logger name (usually __name__)

    Returns:
        Configured logger instance
    """
    return logging.getLogger(name)
