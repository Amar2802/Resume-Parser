import os
from logging.config import fileConfig
from sqlalchemy import create_engine, pool
from alembic import context

from Backend.models import db

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = db.metadata

def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = os.environ.get('DATABASE_URL')
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
    db_url = os.environ.get('DATABASE_URL')
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