"""
Database connection and session management.

Uses SQLAlchemy AsyncEngine with asyncpg dialect for async PostgreSQL connections.
"""
from collections.abc import AsyncGenerator
from typing import Any

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession

from app.config import get_settings

# Global async engine and session factory
_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """
    Get or create the async database engine.
    
    Returns:
        AsyncEngine: SQLAlchemy async engine
        
    Raises:
        RuntimeError: If engine is not initialized
    """
    global _engine
    if _engine is None:
        raise RuntimeError(
            "Database engine not initialized. "
            "Call init_db_engine() on application startup."
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """
    Get the session factory.
    
    Returns:
        async_sessionmaker: Session factory
        
    Raises:
        RuntimeError: If factory is not initialized
    """
    global _session_factory
    if _session_factory is None:
        raise RuntimeError(
            "Session factory not initialized. "
            "Call init_db_engine() on application startup."
        )
    return _session_factory


async def init_db_engine() -> None:
    """
    Initialize the async database engine.

    Creates an AsyncEngine with asyncpg dialect and connection pooling.
    Called on application startup.
    """
    global _engine, _session_factory

    settings = get_settings()

    # Convert URL for asyncpg if needed and remove sslmode parameter
    db_url = settings.database_url
    if not db_url.startswith('postgresql+asyncpg://'):
        db_url = db_url.replace('postgresql://', 'postgresql+asyncpg://')
    
    # Remove sslmode from URL (asyncpg doesn't support it in URL string)
    db_url = db_url.replace('?sslmode=require', '').replace('&sslmode=require', '')

    # Create async engine with pool configuration
    # For Neon/SSL connections, use connect_args
    _engine = create_async_engine(
        db_url,
        echo=settings.debug,  # Enable SQL logging in debug mode
        pool_size=20,
        max_overflow=10,
        pool_pre_ping=True,  # Enable connection health checks
        pool_recycle=300,  # Recycle connections after 5 minutes
        connect_args={
            "ssl": True,  # Enable SSL for Neon
            "server_settings": {
                "application_name": "cs_fte_backend",
            },
        },
    )
    
    # Create session factory
    _session_factory = async_sessionmaker(
        bind=_engine,
        class_=AsyncSession,
        autocommit=False,
        autoflush=False,
        expire_on_commit=False,
    )
    
    print(f"✅ Database engine created: {settings.postgres_host}")


async def close_db_engine() -> None:
    """
    Close the async database engine.
    
    Called on application shutdown.
    """
    global _engine
    if _engine:
        await _engine.dispose()
        print("✅ Database engine closed")


async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Get async database session for FastAPI dependency injection.
    
    Usage:
        @app.get("/")
        async def read_items(db: AsyncSession = Depends(get_db_session)):
            ...
    
    Yields:
        AsyncSession: SQLModel async session
    """
    factory = get_session_factory()
    async with factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


async def create_tables() -> None:
    """
    Create all database tables.
    
    Note: In production, use Alembic migrations instead.
    """
    engine = get_engine()
    
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
