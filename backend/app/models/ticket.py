"""
Ticket model - Customer support ticket entity.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.customer import Customer
    from app.models.conversation import Conversation
    from app.models.escalation import Escalation


class Ticket(SQLModel, table=True):
    """
    Ticket entity representing a customer support ticket.
    
    Attributes:
        id: UUID primary key
        customer_id: Reference to customer
        conversation_id: Reference to conversation
        status: Ticket status
        priority: Priority level
        category: Ticket category
        subject: Ticket subject
        sentiment_score: Sentiment analysis score
        confidence_score: AI confidence score
        assigned_to: Assigned agent email
        created_at: Timestamp
        resolved_at: Resolution timestamp
    """
    __tablename__ = "tickets"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique ticket identifier"
    )
    
    customer_id: uuid.UUID = Field(
        ...,
        foreign_key="customers.id",
        ondelete="CASCADE",
        index=True,
        description="Reference to customer"
    )
    
    conversation_id: Optional[uuid.UUID] = Field(
        default=None,
        foreign_key="conversations.id",
        ondelete="SET NULL",
        index=True,
        description="Reference to conversation"
    )
    
    status: str = Field(
        default="open",
        max_length=50,
        index=True,
        description="Ticket status (open, in_progress, waiting_customer, resolved, escalated, closed)"
    )
    
    priority: str = Field(
        default="normal",
        max_length=20,
        index=True,
        description="Priority level (low, normal, high, urgent)"
    )
    
    category: Optional[str] = Field(
        default=None,
        max_length=100,
        index=True,
        description="Ticket category"
    )
    
    subject: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Ticket subject"
    )
    
    sentiment_score: Optional[float] = Field(
        default=None,
        ge=-1.0,
        le=1.0,
        description="Sentiment analysis score (-1.0 to 1.0)"
    )
    
    confidence_score: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="AI confidence score (0.0 to 1.0)"
    )
    
    assigned_to: Optional[str] = Field(
        default=None,
        max_length=255,
        index=True,
        description="Assigned agent email"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,
        description="Record creation timestamp"
    )
    
    resolved_at: Optional[datetime] = Field(
        default=None,
        description="Resolution timestamp"
    )
    
    # Relationships
    customer: "Customer" = Relationship(back_populates="tickets")
    conversation: Optional["Conversation"] = Relationship(back_populates="ticket")
    escalation: Optional["Escalation"] = Relationship(
        back_populates="ticket",
        sa_relationship_kwargs={"uselist": False}
    )
    
    def __repr__(self) -> str:
        return f"<Ticket(id={self.id}, customer_id={self.customer_id}, status={self.status})>"
