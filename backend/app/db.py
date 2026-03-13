"""
Database migration utilities.

Usage:
    python -m app.db init      # Initialize database (create all tables)
    python -m app.db migrate   # Run pending migrations
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlmodel import SQLModel, select
from app.config import get_settings
from app.models import AIProvider  # noqa: F401


async def init_db():
    """
    Initialize database by creating all tables.
    
    Note: In production, use Alembic migrations instead.
    """
    settings = get_settings()
    
    # Create async engine
    engine = create_async_engine(
        settings.database_url,
        echo=True,
        future=True,
    )
    
    # Create all tables
    async with engine.begin() as conn:
        # Create pgvector extension
        await conn.execute("CREATE EXTENSION IF NOT EXISTS vector")
        
        # Create all SQLModel tables
        await conn.run_sync(SQLModel.metadata.create_all)
    
    print("✅ Database initialized successfully!")
    
    # Initialize AI providers
    await init_ai_providers(engine)
    
    await engine.dispose()


async def init_ai_providers(engine):
    """Initialize default AI providers."""
    async with AsyncSession(engine) as session:
        # Check if providers already exist
        result = await session.exec(select(AIProvider))
        providers = result.all()
        
        if providers:
            print("ℹ️  AI providers already exist, skipping initialization")
            return
        
        # Create default providers
        providers = [
            AIProvider(
                id=1,
                name="openai",
                priority=1,
                is_active=True,
                daily_token_limit=100000,
            ),
            AIProvider(
                id=2,
                name="gemini",
                priority=2,
                is_active=True,
                daily_token_limit=100000,
            ),
            AIProvider(
                id=3,
                name="qwen",
                priority=3,
                is_active=True,
                daily_token_limit=100000,
            ),
        ]
        
        for provider in providers:
            session.add(provider)
        
        await session.commit()
        print("✅ AI providers initialized (OpenAI, Gemini, Qwen)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python -m app.db [init|migrate]")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == "init":
        asyncio.run(init_db())
    elif command == "migrate":
        print("Use 'alembic upgrade head' to run migrations")
        sys.exit(0)
    else:
        print(f"Unknown command: {command}")
        print("Usage: python -m app.db [init|migrate]")
        sys.exit(1)
