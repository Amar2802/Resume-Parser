import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

# --- Make sure this import points to your models file ---
from Backend.models import db
# ----------------------------------------------------

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = db.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = "postgresql://postgres:postgres@localhost:5432/resumes"
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""

    # --- THIS PRINT STATEMENT WILL PROVE THE FILE IS SAVED ---
    print(">>> Running migrations with the new, hardcoded URL! <<<")
    # ---------------------------------------------------------

    db_url = "postgresql://postgres:postgres@localhost:5432/resumes"
    connectable = create_engine(db_url)

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()