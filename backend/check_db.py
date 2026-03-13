"""
Quick database check script.

Shows current tickets, customers, conversations.

Usage:
    cd backend
    .venv\Scripts\activate
    python check_db.py
"""
import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.database import init_db_engine, get_engine
from sqlalchemy import text


async def check_database():
    """Check database contents."""
    print("=" * 60)
    print("Database Contents")
    print("=" * 60)
    
    try:
        await init_db_engine()
        engine = get_engine()
        
        async with engine.begin() as conn:
            # Check customers
            result = await conn.execute(text("SELECT COUNT(*) as count FROM customers"))
            count = result.fetchone()[0]
            print(f"\nCUSTOMERS: {count} records")
            
            result = await conn.execute(text("SELECT id, email, name, created_at FROM customers ORDER BY created_at DESC LIMIT 5"))
            for row in result.fetchall():
                print(f"  - {row[0]} | {row[1]} | {row[2]}")
            
            # Check conversations
            result = await conn.execute(text("SELECT COUNT(*) as count FROM conversations"))
            count = result.fetchone()[0]
            print(f"\nCONVERSATIONS: {count} records")
            
            result = await conn.execute(text("SELECT id, customer_id, status, channel FROM conversations ORDER BY created_at DESC LIMIT 5"))
            for row in result.fetchall():
                print(f"  - {row[0]} | customer: {row[1]} | {row[2]} | {row[3]}")
            
            # Check tickets
            result = await conn.execute(text("SELECT COUNT(*) as count FROM tickets"))
            count = result.fetchone()[0]
            print(f"\nTICKETS: {count} records")
            
            result = await conn.execute(text("""
                SELECT 
                    t.id, 
                    t.customer_id, 
                    t.conversation_id,
                    t.status,
                    t.subject,
                    t.created_at
                FROM tickets t 
                ORDER BY t.created_at DESC 
                LIMIT 5
            """))
            for row in result.fetchall():
                print(f"  - {row[0]} | cust: {row[1]} | conv: {row[2]} | {row[3]} | {row[4]}")
            
            # Check messages
            result = await conn.execute(text("SELECT COUNT(*) as count FROM messages"))
            count = result.fetchone()[0]
            print(f"\nMESSAGES: {count} records")
            
            result = await conn.execute(text("SELECT id, conversation_id, content, role FROM messages ORDER BY created_at DESC LIMIT 5"))
            for row in result.fetchall():
                print(f"  - {row[0]} | conv: {row[1]} | {row[2][:50]}... | {row[3]}")
            
            print("\n" + "=" * 60)
            
    except Exception as e:
        print(f"\nERROR: {e}")
        raise
    finally:
        from app.database import close_db_engine
        await close_db_engine()


if __name__ == "__main__":
    asyncio.run(check_database())
