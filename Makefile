.PHONY: help install run shell lint format type-check check test test-cov clean

# Default target - show help
help:
	@echo "DhakaCart API - Development Commands"
	@echo ""
	@echo "Setup:"
	@echo "  make install       Install all dependencies"
	@echo ""
	@echo "Development:"
	@echo "  make run          Run server with auto-reload"
	@echo "  make shell        Open Python shell"
	@echo ""
	@echo "Code Quality:"
	@echo "  make lint         Run ruff linter"
	@echo "  make format       Format code with ruff"
	@echo "  make type-check   Run mypy type checker"
	@echo "  make check        Run all checks (lint + format + type)"
	@echo ""
	@echo "Testing:"
	@echo "  make test         Run tests"
	@echo "  make test-cov     Run tests with coverage report"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean        Remove cache and temp files"

# Install all dependencies (dev mode by default)
install:
	uv sync

# Run server with auto-reload
run:
	uv run uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload

# Open Python shell
shell:
	uv run python

# Run linter
lint:
	uv run ruff check .

# Format code
format:
	uv run ruff format .

# Type check
type-check:
	uv run mypy src/

# Run all checks
check: lint type-check
	@echo "✓ All checks passed!"

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term

# Clean cache and temporary files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf htmlcov/
	rm -rf .coverage
	@echo "✓ Cleaned all cache and temporary files"