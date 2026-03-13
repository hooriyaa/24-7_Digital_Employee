"""
Alembic migrations environment configuration.

Configured for:
- Async database connections with asyncpg
- SQLModel metadata autogenerate
- pgvector extension support
"""
from logging.config import fileConfig

from sqlalchemy import pool, event
from sqlalchemy.engine import Engine
from sqlalchemy import create_engine
from alembic import context

# Import SQLModel and all models for metadata discovery
from sqlmodel import SQLModel
from app.models import (  # noqa: F401
    Customer,
    Channel,
    ChannelIdentity,
    Conversation,
    Message,
    Ticket,
    Escalation,
    AIProvider,
    KnowledgeBase,
)

# Import pgvector for Vector type support
from pgvector.sqlalchemy import Vector  # noqa: F401

# this is the Alembic Config object
config = context.config

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata to SQLModel's metadata for autogenerate support
target_metadata = SQLModel.metadata

# Get database URL from environment or config
import os
from dotenv import load_dotenv
from pathlib import Path

# Load .env file
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    config.get_main_option("sqlalchemy.url")
)

# Convert async URL to sync URL for Alembic
# asyncpg -> psycopg2 for migrations
def get_sync_url(async_url: str) -> str:
    """Convert async database URL to sync URL for Alembic."""
    return async_url.replace("postgresql+asyncpg://", "postgresql://")


def run_migrations_offline() -> None:
    """
    Run migrations in 'offline' mode.
    
    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well. By skipping the Engine creation
    we don't even need a DBAPI to be available.
    
    Calls to context.execute() here emit the given string to the
    script output.
    """
    url = get_sync_url(DATABASE_URL)
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        render_as_batch=True,  # Enable batch mode for SQLite compatibility
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """
    Run migrations in 'online' mode.
    
    Creates a sync engine and runs migrations.
    Alembic uses synchronous connections for migrations.
    """
    # Convert async URL to sync URL
    sync_url = get_sync_url(DATABASE_URL)
    
    # Create sync engine for migrations
    connectable = create_engine(
        sync_url,
        poolclass=pool.NullPool,
        echo=False,  # Set to True for SQL debugging
        future=True,
    )

    # Register pgvector extension creation
    @event.listens_for(connectable, "connect")
    def register_vector_type(dbapi_connection, branch):
        """Register pgvector extension on connection."""
        if branch:
            return
        with dbapi_connection.cursor():
            dbapi_connection.execute("CREATE EXTENSION IF NOT EXISTS vector")

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            render_as_batch=True,  # Enable batch mode for better compatibility
            compare_type=True,  # Compare column types
            compare_server_default=True,  # Compare server defaults
        )

        with context.begin_transaction():
            context.run_migrations()

    # Dispose engine to clean up connections
    connectable.dispose()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
