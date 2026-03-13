"""
KnowledgeBase model - Knowledge base with pgvector embedding for RAG.
"""
import uuid
from datetime import datetime
from typing import Optional, List

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, JSON
from sqlmodel import Field, SQLModel


class KnowledgeBase(SQLModel, table=True):
    """
    KnowledgeBase entity for storing RAG knowledge with vector embeddings.
    
    Used for Context7 documentation and custom knowledge base.
    
    Attributes:
        id: UUID primary key
        title: Document title
        content: Document content
        source: Content source (context7, custom, url)
        url: Source URL (if applicable)
        embedding: Vector embedding for semantic search (1536 dimensions)
        metadata: Additional metadata (tags, category, etc.)
        is_active: Whether document is active
        created_at: Timestamp
        updated_at: Timestamp
    """
    __tablename__ = "knowledge_base"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique knowledge base entry identifier"
    )
    
    title: str = Field(
        ...,
        max_length=500,
        index=True,
        description="Document title"
    )
    
    content: str = Field(
        ...,
        description="Document content"
    )
    
    source: str = Field(
        default="custom",
        max_length=50,
        index=True,
        description="Content source (context7, custom, url)"
    )
    
    url: Optional[str] = Field(
        default=None,
        max_length=2048,
        description="Source URL (if applicable)"
    )
    
    # pgvector embedding column for semantic search
    # Uses 1536 dimensions for OpenAI text-embedding-ada-002
    embedding: Optional[List[float]] = Field(
        default=None,
        sa_column=Column(Vector(1536)),
        description="Vector embedding for semantic search (1536 dimensions)"
    )
    
    tags: list = Field(
        default=[],
        sa_type=JSON,
        description="Tags for categorization"
    )
    
    category: Optional[str] = Field(
        default=None,
        max_length=100,
        index=True,
        description="Category for organization"
    )
    
    custom_metadata: dict = Field(
        default={},
        sa_type=JSON,
        description="Additional metadata"
    )
    
    is_active: bool = Field(
        default=True,
        index=True,
        description="Whether document is active"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Record creation timestamp"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record last update timestamp"
    )
    
    def __repr__(self) -> str:
        return f"<KnowledgeBase(id={self.id}, title={self.title}, source={self.source})>"
