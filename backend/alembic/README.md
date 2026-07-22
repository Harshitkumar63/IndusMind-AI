# Alembic Database Migrations

This directory contains Alembic database migration scripts for IndusMind AI.

## Setup

```bash
cd backend
pip install alembic
alembic init alembic
```

## Commands

```bash
# Create a new migration from model changes
alembic revision --autogenerate -m "describe your change"

# Apply all pending migrations
alembic upgrade head

# Roll back one revision
alembic downgrade -1

# Show migration history
alembic history

# Show current revision
alembic current
```

## Workflow

1. Modify your SQLAlchemy models in `app/domain/models/`
2. Run `alembic revision --autogenerate -m "your description"`
3. Review the generated file in `alembic/versions/`
4. Apply with `alembic upgrade head`
5. Commit both the model change and migration file

## Environment

Alembic reads `DATABASE_URL` from your `.env` file via `app/core/config.py`.
