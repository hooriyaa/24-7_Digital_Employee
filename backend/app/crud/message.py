"""
Message CRUD operations.
"""
import uuid
from typing import Any

from pydantic import BaseModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.message import Message


class MessageCreate(BaseModel):
    """Message creation schema."""
    conversation_id: uuid.UUID = Field(..., description="Conversation ID")
    sender_type: str = Field(..., description="Sender type (customer/agent/system)")
    channel: str = Field(..., description="Channel (gmail/whatsapp/web)")
    content: str = Field(..., description="Message content")
    role: str = Field(default="user", description="Message role")
    sentiment_score: float | None = Field(default=None, description="Sentiment score")


class MessageUpdate(BaseModel):
    """Message update schema."""
    content: str | None = Field(default=None, description="Message content")
    content_embedding: list[float] | None = Field(default=None, description="Vector embedding")


class CRUDMessage(CRUDBase[Message, MessageCreate, MessageUpdate]):
    """
    Message CRUD operations.
    
    Extends base CRUD with message-specific methods.
    """
    
    async def get_by_conversation(
        self,
        session: AsyncSession,
        conversation_id: uuid.UUID,
        limit: int = 50
    ) -> list[Message]:
        """
        Get messages for a conversation.

        Args:
            session: Async database session
            conversation_id: Conversation ID
            limit: Maximum messages to return

        Returns:
            List of messages ordered by creation time (oldest first)
        """
        from sqlalchemy import select
        
        stmt = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at.asc()).limit(limit)
        
        result = await session.execute(stmt)
        return list(result.scalars().all())
    
    async def get_last_message(
        self,
        session: AsyncSession,
        conversation_id: uuid.UUID
    ) -> Message | None:
        """
        Get the last message in a conversation.
        
        Args:
            session: Async database session
            conversation_id: Conversation ID
            
        Returns:
            Last message or None
        """
        messages = await self.get_by_conversation(session, conversation_id, limit=1)
        return messages[0] if messages else None
    
    async def create_with_embedding(
        self,
        session: AsyncSession,
        *,
        obj_in: MessageCreate,
        embedding: list[float] | None = None
    ) -> Message:
        """
        Create a message with vector embedding.
        
        Args:
            session: Async database session
            obj_in: Message creation schema
            embedding: Optional vector embedding
            
        Returns:
            Created message
        """
        db_obj = Message(
            conversation_id=obj_in.conversation_id,
            sender_type=obj_in.sender_type,
            channel=obj_in.channel,
            content=obj_in.content,
            role=obj_in.role,
            content_embedding=embedding,
        )
        
        session.add(db_obj)
        await session.commit()
        await session.refresh(db_obj)
        return db_obj


# Singleton instance
message_crud = CRUDMessage(Message)
