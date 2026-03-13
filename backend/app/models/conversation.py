"""
Conversation model - Conversation thread within a ticket.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.ticket import Ticket
    from app.models.message import Message


class Conversation(SQLModel, table=True):
    """
    Conversation entity representing a conversation thread.
    
    Attributes:
        id: UUID primary key
        customer_id: Reference to customer
        status: Conversation status
        sentiment_score: Overall sentiment (-1.0 to 1.0)
        message_count: Number of messages in conversation
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    __tablename__ = "conversations"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique conversation identifier"
    )
    
    customer_id: uuid.UUID = Field(
        ...,
        foreign_key="customers.id",
        ondelete="CASCADE",
        index=True,
        description="Reference to customer"
    )
    
    status: str = Field(
        default="active",
        max_length=50,
        index=True,
        description="Conversation status (active, archived, closed)"
    )
    
    sentiment_score: Optional[float] = Field(
        default=None,
        ge=-1.0,
        le=1.0,
        description="Overall conversation sentiment (-1.0 to 1.0)"
    )
    
    message_count: int = Field(
        default=0,
        ge=0,
        description="Number of messages in conversation"
    )
    
    last_message_at: Optional[datetime] = Field(
        default=None,
        description="Timestamp of last message"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record last update timestamp"
    )
    
    # Relationships
    messages: list["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={
            "cascade": "all, delete-orphan",
            "order_by": "Message.created_at.asc()"
        }
    )
    
    ticket: "Ticket" = Relationship(back_populates="conversation")
    
    def __repr__(self) -> str:
        return f"<Conversation(id={self.id}, customer_id={self.customer_id})>"
