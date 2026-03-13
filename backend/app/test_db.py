"""
Database connection test script.

Verifies that the database tables were created successfully.
"""
import asyncio
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncConnection
from app.config import get_settings


async def test_database():
    """Test database connection and verify tables exist."""
    settings = get_settings()
    
    # Convert to async URL if needed and remove sslmode for asyncpg
    db_url = settings.database_url
    if not db_url.startswith('postgresql+asyncpg://'):
        db_url = db_url.replace('postgresql://', 'postgresql+asyncpg://')
    
    # Remove sslmode from URL for asyncpg (it handles SSL automatically)
    db_url = db_url.replace('?sslmode=require', '')
    
    print(f"Connecting to: {db_url.replace(settings.postgres_password, '***')}")
    
    # Create async engine with SSL support for Neon
    engine = create_async_engine(
        db_url,
        echo=True,
        future=True,
        connect_args={"ssl": "require"},
    )
    
    try:
        async with engine.connect() as conn:
            # Test connection
            result = await conn.execute(text("SELECT 1"))
            print("Database connection successful!")

            # List all tables
            result = await conn.execute(text("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                AND table_type = 'BASE TABLE'
                ORDER BY table_name
            """))
            tables = [row[0] for row in result.fetchall()]

            print(f"Tables found ({len(tables)}):")
            for table in tables:
                print(f"  - {table}")

            # Verify expected tables
            expected_tables = [
                'customers',
                'channels',
                'channel_identities',
                'conversations',
                'messages',
                'tickets',
                'escalations',
                'ai_providers',
                'knowledge_base',
                'alembic_version',
            ]

            print("Verifying expected tables:")
            missing = []
            for table in expected_tables:
                if table in tables:
                    print(f"  [OK] {table}")
                else:
                    print(f"  [MISSING] {table}")
                    missing.append(table)
            
            # Check pgvector extension
            result = await conn.execute(text("""
                SELECT extname FROM pg_extension WHERE extname = 'vector'
            """))
            extensions = [row[0] for row in result.fetchall()]
            
            if 'vector' in extensions:
                print("pgvector extension installed!")
            else:
                print("pgvector extension NOT found!")
            
            # Test Vector type by querying knowledge_base structure
            result = await conn.execute(text("""
                SELECT column_name, data_type, udt_name
                FROM information_schema.columns
                WHERE table_name = 'knowledge_base'
                AND column_name = 'embedding'
            """))
            columns = result.fetchall()
            
            if columns:
                print("knowledge_base.embedding column exists!")
                for col in columns:
                    print(f"   Column: {col.column_name}, Type: {col.udt_name}")
            else:
                print("knowledge_base.embedding column NOT found!")
            
            # Summary
            print("=" * 50)
            if not missing and 'vector' in extensions:
                print("SUCCESS: All tables and extensions verified!")
                return True
            else:
                print("WARNING: Some tables or extensions are missing!")
                return False
                
    except Exception as e:
        print(f"Error: {e}")
        return False
    finally:
        await engine.dispose()


if __name__ == "__main__":
    print("=" * 50)
    print("Database Connection Test")
    print("=" * 50)
    
    success = asyncio.run(test_database())
    
    print("=" * 50)
    if success:
        print("Result: PASSED")
    else:
        print("Result: FAILED")
    print("=" * 50)
