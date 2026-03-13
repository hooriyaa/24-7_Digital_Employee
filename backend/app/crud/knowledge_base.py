"""
KnowledgeBase CRUD operations.
"""
import uuid
import os
from typing import Any
import re

from pydantic import BaseModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import text

from app.crud.base import CRUDBase
from app.models.knowledge_base import KnowledgeBase


class KnowledgeBaseCreate(BaseModel):
    """Knowledge base entry creation schema."""
    title: str = Field(..., description="Entry title")
    content: str = Field(..., description="Entry content")
    source: str = Field(default="custom", description="Content source")
    url: str | None = Field(default=None, description="Source URL")
    category: str | None = Field(default=None, description="Category")
    tags: list[str] = Field(default=[], description="Tags")


class KnowledgeBaseUpdate(BaseModel):
    """Knowledge base entry update schema."""
    title: str | None = Field(default=None, description="Entry title")
    content: str | None = Field(default=None, description="Entry content")
    is_active: bool | None = Field(default=None, description="Active status")
    category: str | None = Field(default=None, description="Category")
    tags: list[str] | None = Field(default=None, description="Tags")


class CRUDKnowledgeBase(CRUDBase[KnowledgeBase, KnowledgeBaseCreate, KnowledgeBaseUpdate]):
    """
    KnowledgeBase CRUD operations.

    Extends base CRUD with knowledge base-specific methods.
    """

    async def search_similar(
        self,
        session: AsyncSession,
        query: str,
        limit: int = 3
    ) -> list[dict]:
        """
        Search knowledge base using simple text matching.
        
        Falls back to reading from product_info.txt file.

        Args:
            session: Async database session
            query: Search query
            limit: Maximum results to return

        Returns:
            List of dicts with title, content, and similarity score
        """
        print(f"📚 [KNOWLEDGE_BASE] Searching for: {query}")
        
        # Try database search first using text search
        try:
            result = await session.exec(
                text("""
                    SELECT id, title, content, 
                           ts_rank(to_tsvector('english', content), plainto_tsquery('english', :query)) as similarity
                    FROM knowledge_base
                    WHERE is_active = true
                      AND to_tsvector('english', content) @@ plainto_tsquery('english', :query)
                    ORDER BY similarity DESC
                    LIMIT :limit
                """).bindparams(query=query, limit=limit)
            )
            
            rows = result.all()
            if rows:
                results = [
                    {
                        "id": str(row.id),
                        "title": row.title,
                        "content": row.content,
                        "similarity": float(row.similarity) if row.similarity else 0.0,
                    }
                    for row in rows
                ]
                print(f"📚 [KNOWLEDGE_BASE] Found {len(results)} results in database")
                return results
        except Exception as e:
            print(f"⚠️  [KNOWLEDGE_BASE] Database search failed: {e}")
        
        # Fallback: Read from product_info.txt
        print(f"📚 [KNOWLEDGE_BASE] Fallback to product_info.txt")
        return self._search_product_info_file(query, limit)
    
    def _search_product_info_file(self, query: str, limit: int = 5) -> list[dict]:
        """
        Search product_info.txt file for relevant content.

        Uses flexible keyword matching - if ANY keyword matches, include that section.

        Args:
            query: Search query
            limit: Maximum results to return (increased to 5 for better coverage)

        Returns:
            List of dicts with title, content, and similarity score
        """
        product_info_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)),
            "data",
            "docs",
            "product_info.txt"
        )

        print(f"📚 [KNOWLEDGE_BASE] Reading from: {product_info_path}")

        if not os.path.exists(product_info_path):
            print(f"❌ [KNOWLEDGE_BASE] File not found: {product_info_path}")
            return []

        try:
            with open(product_info_path, "r", encoding="utf-8") as f:
                content = f.read()

            # Parse markdown-style sections
            sections = self._parse_markdown_sections(content)

            # Flexible keyword matching - ANY keyword match includes the section
            query_lower = query.lower()
            query_keywords = [word for word in query_lower.split() if len(word) > 2]
            results = []

            for title, section_content in sections:
                section_lower = section_content.lower()
                title_lower = title.lower()
                
                # Check for ANY keyword match in title or content
                keyword_matches = sum(1 for keyword in query_keywords if keyword in title_lower or keyword in section_lower)
                
                # Title match gets higher priority
                title_match = 2.0 if query_lower in title_lower else (0.5 if any(kw in title_lower for kw in query_keywords) else 0.0)
                
                # Content match score based on keyword coverage
                content_match = keyword_matches * 0.2
                
                similarity = title_match + content_match

                # Include section if ANY keyword matches (lowered threshold)
                if keyword_matches > 0 or query_lower in title_lower:
                    results.append({
                        "title": title,
                        "content": section_content,  # Return FULL content, not truncated
                        "similarity": similarity,
                        "keyword_matches": keyword_matches,
                    })

            # Sort by similarity and return top results
            results.sort(key=lambda x: x["similarity"], reverse=True)
            print(f"📚 [KNOWLEDGE_BASE] Found {len(results)} results in product_info.txt")
            return results[:limit]

        except Exception as e:
            print(f"❌ [KNOWLEDGE_BASE] Error reading product_info.txt: {e}")
            return []
    
    def _parse_markdown_sections(self, content: str) -> list[tuple[str, str]]:
        """
        Parse markdown content into sections.
        
        Args:
            content: Markdown content
            
        Returns:
            List of (title, content) tuples
        """
        sections = []
        current_title = "Overview"
        current_content = []
        
        for line in content.split("\n"):
            if line.startswith("## "):
                # Save previous section
                if current_content:
                    sections.append((current_title, "\n".join(current_content)))
                
                # Start new section
                current_title = line[3:].strip()
                current_content = []
            else:
                current_content.append(line)
        
        # Save last section
        if current_content:
            sections.append((current_title, "\n".join(current_content)))
        
        return sections

    async def search_by_title(
        self,
        session: AsyncSession,
        title_query: str,
        limit: int = 10
    ) -> list[KnowledgeBase]:
        """
        Search knowledge base by title.

        Args:
            session: Async database session
            title_query: Title search query
            limit: Maximum results to return

        Returns:
            List of matching entries
        """
        return await self.get_multi(
            session,
            filters={"is_active": True},
            limit=limit,
        )

    async def get_by_category(
        self,
        session: AsyncSession,
        category: str
    ) -> list[KnowledgeBase]:
        """
        Get knowledge base entries by category.

        Args:
            session: Async database session
            category: Category name

        Returns:
            List of entries in category
        """
        return await self.get_multi(
            session,
            filters={"category": category, "is_active": True},
            limit=100,
        )

    async def get_active_entries(
        self,
        session: AsyncSession,
        limit: int = 100
    ) -> list[KnowledgeBase]:
        """
        Get all active knowledge base entries.

        Args:
            session: Async database session
            limit: Maximum entries to return

        Returns:
            List of active entries
        """
        return await self.get_multi(
            session,
            filters={"is_active": True},
            limit=limit,
        )


# Singleton instance
knowledge_base_crud = CRUDKnowledgeBase(KnowledgeBase)
