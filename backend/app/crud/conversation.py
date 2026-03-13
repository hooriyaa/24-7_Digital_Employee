"""
Conversation CRUD operations.
"""
import uuid
from typing import Any

from pydantic import BaseModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.conversation import Conversation


class ConversationCreate(BaseModel):
    """Conversation creation schema."""
    customer_id: uuid.UUID = Field(..., description="Customer ID")
    status: str = Field(default="active", description="Conversation status")
    channel: str = Field(default="web", description="Communication channel")


class ConversationUpdate(BaseModel):
    """Conversation update schema."""
    status: str | None = Field(default=None, description="Conversation status")
    sentiment_score: float | None = Field(default=None, description="Sentiment score")
    message_count: int | None = Field(default=None, description="Message count")
    last_message_at: Any | None = Field(default=None, description="Last message timestamp")


class CRUDConversation(CRUDBase[Conversation, ConversationCreate, ConversationUpdate]):
    """
    Conversation CRUD operations.

    Extends base CRUD with conversation-specific methods.
    """

    async def get_by_customer(
        self,
        session: AsyncSession,
        customer_id: uuid.UUID,
        limit: int = 10
    ) -> list[Conversation]:
        """
        Get conversations for a customer.

        Args:
            session: Async database session
            customer_id: Customer ID
            limit: Maximum conversations to return

        Returns:
            List of conversations ordered by creation time
        """
        return await self.get_multi(
            session,
            filters={"customer_id": customer_id},
            offset=0,
            limit=limit,
        )

    async def get_active_conversation(
        self,
        session: AsyncSession,
        customer_id: uuid.UUID
    ) -> Conversation | None:
        """
        Get the active conversation for a customer.

        Args:
            session: Async database session
            customer_id: Customer ID

        Returns:
            Active conversation or None
        """
        conversations = await self.get_multi(
            session,
            filters={"customer_id": customer_id, "status": "active"},
            limit=1,
        )
        return conversations[0] if conversations else None


# Singleton instance
conversation_crud = CRUDConversation(Conversation)
