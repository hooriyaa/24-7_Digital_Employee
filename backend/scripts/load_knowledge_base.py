#!/usr/bin/env python3
"""
Load context files into knowledge base.

This script reads all markdown files from the context/ folder
and loads them into the PostgreSQL knowledge_base table.
"""

import asyncio
import asyncpg
from pathlib import Path
import json
import sys


async def load_knowledge_base():
    """Load all context files into the database."""
    
    print("Connecting to database...")
    try:
        conn = await asyncpg.connect(
            "postgresql://postgres:postgres@localhost:5432/crm_db"
        )
        print("OK Connected to database")
    except Exception as e:
        print(f"ERROR Failed to connect to database: {e}")
        print("Make sure PostgreSQL is running and credentials are correct")
        sys.exit(1)
    
    context_dir = Path(__file__).parent.parent / "context"
    
    if not context_dir.exists():
        print(f"ERROR Context directory not found: {context_dir}")
        sys.exit(1)
    
    print(f"Loading files from: {context_dir}")
    
    files_loaded = 0
    sections_loaded = 0
    
    # Load markdown files
    for md_file in context_dir.glob("*.md"):
        print(f"\nLoading {md_file.name}...")
        
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Split into sections (by ## headers)
            sections = content.split('## ')
            
            for i, section in enumerate(sections):
                if not section.strip():
                    continue
                
                # Extract title from first line
                lines = section.split('\n')
                title = lines[0].strip()
                
                # Create record
                await conn.execute("""
                    INSERT INTO knowledge_base (title, content, category, tags)
                    VALUES ($1, $2, $3, $4)
                    ON CONFLICT DO NOTHING
                """, 
                    f"{md_file.stem}: {title[:100]}",
                    section,
                    md_file.stem,
                    [md_file.stem, 'knowledge_base']
                )
                
                sections_loaded += 1
            
            files_loaded += 1
            print(f"   OK Loaded {len(sections)} sections from {md_file.name}")
            
        except Exception as e:
            print(f"   WARNING Error loading {md_file.name}: {e}")
    
    # Load sample tickets
    tickets_file = context_dir / "sample-tickets.json"
    if tickets_file.exists():
        print(f"\nLoading sample-tickets.json...")
        try:
            with open(tickets_file, 'r', encoding='utf-8') as f:
                tickets = json.load(f)
            
            for ticket in tickets:
                await conn.execute("""
                    INSERT INTO sample_tickets (data, category)
                    VALUES ($1, $2)
                    ON CONFLICT DO NOTHING
                """, json.dumps(ticket), 'training')
            
            print(f"   OK Loaded {len(tickets)} sample tickets")
            files_loaded += 1
            
        except Exception as e:
            print(f"   WARNING Error loading sample tickets: {e}")
    
    await conn.close()
    
    print(f"\n{'='*60}")
    print(f"KNOWLEDGE BASE LOADED SUCCESSFULLY!")
    print(f"{'='*60}")
    print(f"Summary:")
    print(f"   - Files processed: {files_loaded}")
    print(f"   - Sections loaded: {sections_loaded}")
    print(f"   - Location: PostgreSQL knowledge_base table")
    print(f"\nNext steps:")
    print(f"   1. Restart backend server")
    print(f"   2. Test AI with: python test_agent.py")
    print(f"   3. Submit a ticket from frontend")
    print(f"{'='*60}\n")


if __name__ == "__main__":
    asyncio.run(load_knowledge_base())
