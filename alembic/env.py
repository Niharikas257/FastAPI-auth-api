# alembic/env.py
from __future__ import annotations

import os
import sys
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# ------------------------------------------------------------------------------
# Ensure project root is on PYTHONPATH so "app" imports work when Alembic runs
# This makes env.py location-agnostic (works with `alembic -c alembic.ini ...`)
# ------------------------------------------------------------------------------
HERE = os.path.abspath(os.path.dirname(__file__))               # .../alembic
PROJECT_ROOT = os.path.abspath(os.path.join(HERE, ".."))        # project root
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ------------------------------------------------------------------------------
# Load .env from project root (works in Docker and locally)
# ------------------------------------------------------------------------------
try:
    from dotenv import load_dotenv  # type: ignore
    load_dotenv(dotenv_path=os.path.join(PROJECT_ROOT, ".env"))
except Exception:
    # dotenv is optional; ignore if not installed or .env is missing
    pass

# ------------------------------------------------------------------------------
# Import metadata for autogenerate
# Make sure importing models does not execute app runtime code.
# ------------------------------------------------------------------------------
try:
    from app.database import Base  # declarative_base()
    # Import modules that register models on Base.metadata
    from app import models          # noqa: F401
    from app import models_task     # noqa: F401
except Exception as e:
    raise RuntimeError(
        f"Failed to import metadata/models for Alembic: {e}\n"
        f"PYTHONPATH={sys.path}"
    ) from e

# ------------------------------------------------------------------------------
# Alembic Config
# ------------------------------------------------------------------------------
config = context.config

# Prefer environment DATABASE_URL over alembic.ini
env_url = os.getenv("DATABASE_URL")
if env_url:
    config.set_main_option("sqlalchemy.url", env_url)

# Configure logging (from alembic.ini)
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# The target metadata for 'autogenerate' support
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    if not url:
        raise RuntimeError("No database URL configured for offline migrations.")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,          # detect column type changes
        compare_server_default=True # detect default changes
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    cfg_section = config.get_section(config.config_ini_section) or {}
    # engine_from_config uses sqlalchemy.url from the merged config above
    connectable = engine_from_config(
        cfg_section,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        future=True,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
