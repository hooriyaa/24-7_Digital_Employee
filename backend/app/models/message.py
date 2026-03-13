"""
Message model - Individual message in a conversation with pgvector embedding support.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional, List

from pgvector.sqlalchemy import Vector
from sqlalchemy import Column, JSON
from sqlmodel import Field, Relationship, SQLModel


class Message(SQLModel, table=True):
    """
    Message entity representing an individual message in a conversation.
    
    Includes pgvector embedding for RAG (Retrieval-Augmented Generation).
    
    Attributes:
        id: UUID primary key
        conversation_id: Reference to conversation
        sender_type: Who sent the message (customer, agent, system)
        channel: Channel used (gmail, whatsapp, web)
        role: Message role in conversation
        content: Message content
        content_embedding: Vector embedding for semantic search (1536 dimensions)
        tool_calls: JSON array of tool calls (for AI messages)
        metadata: Additional message data
        created_at: Timestamp
    """
    __tablename__ = "messages"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique message identifier"
    )
    
    conversation_id: uuid.UUID = Field(
        ...,
        foreign_key="conversations.id",
        ondelete="CASCADE",
        index=True,
        description="Reference to conversation"
    )
    
    sender_type: str = Field(
        ...,
        max_length=20,
        index=True,
        description="Sender type (customer, agent, system, ai)"
    )
    
    channel: str = Field(
        ...,
        max_length=50,
        description="Channel used (gmail, whatsapp, web)"
    )
    
    role: str = Field(
        default="user",
        max_length=50,
        description="Message role (user, assistant, system, tool)"
    )
    
    content: str = Field(
        ...,
        description="Message content"
    )
    
    # pgvector embedding column for semantic search
    # Uses 1536 dimensions for OpenAI text-embedding-ada-002
    content_embedding: Optional[List[float]] = Field(
        default=None,
        sa_column=Column(Vector(1536)),
        description="Vector embedding for semantic search (1536 dimensions)"
    )
    
    tool_calls: list = Field(
        default=[],
        sa_type=JSON,
        description="Array of tool calls (for AI messages)"
    )
    
    custom_metadata: dict = Field(
        default={},
        sa_type=JSON,
        description="Additional message metadata"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Record creation timestamp"
    )
    
    # Relationships
    conversation: "Conversation" = Relationship(back_populates="messages")
    
    def __repr__(self) -> str:
        return f"<Message(id={self.id}, conversation_id={self.conversation_id}, sender={self.sender_type})>"
