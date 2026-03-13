"""
Database Cleanup Script

Deletes all dummy/seed data from PostgreSQL.
Use this to start fresh with only form-submitted tickets.

Usage:
    cd backend
    .venv\Scripts\activate
    python app/cleanup_db.py
"""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from sqlalchemy import text
from app.database import init_db_engine, get_engine


async def cleanup_database():
    """Delete all data from tables in correct order (respecting foreign keys)."""
    
    print("🗑️  Starting database cleanup...")
    print("=" * 50)
    
    try:
        # Initialize database engine
        await init_db_engine()
        engine = get_engine()
        
        async with engine.begin() as conn:
            # Delete in reverse order of dependencies
            tables_to_clean = [
                "escalations",
                "messages",
                "conversations",
                "tickets",
                "customers",
                "knowledge_base_articles",
                "ai_providers",
                "channel_identities",
            ]
            
            for table in tables_to_clean:
                try:
                    result = await conn.execute(text(f"DELETE FROM {table}"))
                    row_count = result.rowcount
                    print(f"✅ Deleted {row_count} rows from {table}")
                except Exception as e:
                    print(f"⚠️  Error deleting from {table}: {e}")
            
            # Reset sequences (optional, for auto-increment IDs)
            print("\n🔄 Resetting sequences...")
            sequences = [
                "customers_id_seq",
                "tickets_id_seq",
                "conversations_id_seq",
                "messages_id_seq",
            ]
            
            for seq in sequences:
                try:
                    await conn.execute(text(f"ALTER SEQUENCE {seq} RESTART WITH 1"))
                except Exception:
                    pass  # Sequences might not exist for UUID tables
            
            print("\n" + "=" * 50)
            print("✨ Database cleanup complete!")
            print("=" * 50)
            print("\nYour database is now empty and ready for fresh data.")
            print("Submit tickets via the form at: http://localhost:3000/tickets")
            
    except Exception as e:
        print(f"\n❌ Cleanup failed: {e}")
        print("\nMake sure:")
        print("  1. Database is running")
        print("  2. Connection string in .env is correct")
        print("  3. You have permission to delete data")
        raise
    finally:
        from app.database import close_db_engine
        await close_db_engine()


if __name__ == "__main__":
    print("\n⚠️  WARNING: This will DELETE ALL data from the database!")
    print("Type 'yes' to confirm: ", end="")
    
    # For automated runs, skip confirmation
    if len(sys.argv) > 1 and sys.argv[1] == "--force":
        print("\n--force flag detected, skipping confirmation...")
        asyncio.run(cleanup_database())
    else:
        # Interactive confirmation
        confirm = input().strip().lower()
        if confirm == "yes":
            asyncio.run(cleanup_database())
        else:
            print("\n❌ Cleanup cancelled.")
            print("Run with --force flag to skip confirmation.")
