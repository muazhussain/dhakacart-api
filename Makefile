.PHONY: help install run shell lint format type-check check test test-cov clean
.PHONY: migration migrate migrate-down migrate-history migrate-current
.PHONY: db-init db-reset db-shell docker-db-up docker-db-down docker-db-logs

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
	@echo "Database:"
	@echo "  make migration msg='...'  Create new migration"
	@echo "  make migrate              Run pending migrations"
	@echo "  make migrate-down         Rollback one migration"
	@echo "  make migrate-history      Show migration history"
	@echo "  make migrate-current      Show current version"
	@echo "  make db-init              Initialize database (docker + migrate)"
	@echo "  make db-reset             Reset database (WARNING: deletes data)"
	@echo "  make db-shell             Open PostgreSQL shell"
	@echo ""
	@echo "Docker:"
	@echo "  make docker-db-up         Start PostgreSQL container"
	@echo "  make docker-db-down       Stop containers"
	@echo "  make docker-db-logs       View database logs"
	@echo ""
	@echo "Utilities:"
	@echo "  make clean                Remove cache and temp files"

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
check: format lint type-check
	@echo "✓ All checks passed!"

# Run tests
test:
	uv run pytest

# Run tests with coverage
test-cov:
	uv run pytest --cov=src --cov-report=html --cov-report=term

# ============================================================================
# Database Commands
# ============================================================================

# Create new migration
migration:
	@if [ -z "$(msg)" ]; then \
		echo "❌ Error: msg parameter required"; \
		echo "Usage: make migration msg='your migration message'"; \
		exit 1; \
	fi
	uv run alembic revision --autogenerate -m "$(msg)"

# Run pending migrations
migrate:
	uv run alembic upgrade head

# Rollback one migration
migrate-down:
	uv run alembic downgrade -1

# Show migration history
migrate-history:
	uv run alembic history

# Show current migration version
migrate-current:
	uv run alembic current

# Initialize database (start docker + migrate)
db-init: docker-db-up
	@echo "⏳ Waiting for PostgreSQL to be ready..."
	@sleep 3
	@make migrate
	@echo "✓ Database initialized!"

# Reset database (drop all + re-migrate)
db-reset:
	@echo "⚠️  WARNING: This will delete all data!"
	@read -p "Are you sure? [y/N] " -n 1 -r; \
	echo; \
	if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
		uv run alembic downgrade base; \
		uv run alembic upgrade head; \
		echo "✓ Database reset complete!"; \
	else \
		echo "❌ Reset cancelled."; \
	fi

# Open PostgreSQL shell
db-shell:
	docker exec -it dhakacart-postgres psql -U postgres -d dhakacart_dev

# ============================================================================
# Docker Commands
# ============================================================================

# Start PostgreSQL container
docker-db-up:
	docker compose up -d postgres
	@echo "✓ PostgreSQL started"

# Stop containers
docker-db-down:
	docker compose down
	@echo "✓ Containers stopped"

# View database logs
docker-db-logs:
	docker compose logs -f postgres

# ============================================================================
# Utilities
# ============================================================================

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