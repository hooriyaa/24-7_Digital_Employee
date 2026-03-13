"""
Escalation model - Human escalation records.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.ticket import Ticket


class Escalation(SQLModel, table=True):
    """
    Escalation entity representing a human escalation record.
    
    Attributes:
        id: UUID primary key
        ticket_id: Reference to ticket (unique)
        reason: Escalation reason
        escalated_to: Assigned human agent email
        escalated_at: Escalation timestamp
        resolved_at: Resolution timestamp
        resolution_notes: Resolution notes
    """
    __tablename__ = "escalations"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique escalation identifier"
    )
    
    ticket_id: uuid.UUID = Field(
        ...,
        foreign_key="tickets.id",
        ondelete="CASCADE",
        unique=True,
        index=True,
        description="Reference to ticket (unique)"
    )
    
    reason: str = Field(
        ...,
        max_length=255,
        description="Escalation reason (low_confidence, negative_sentiment, customer_request, complex_issue)"
    )
    
    escalated_to: Optional[str] = Field(
        default=None,
        max_length=255,
        index=True,
        description="Assigned human agent email"
    )
    
    escalated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Escalation timestamp"
    )
    
    resolved_at: Optional[datetime] = Field(
        default=None,
        description="Resolution timestamp"
    )
    
    resolution_notes: Optional[str] = Field(
        default=None,
        description="Resolution notes"
    )
    
    # Relationships
    ticket: "Ticket" = Relationship(back_populates="escalation")
    
    def __repr__(self) -> str:
        return f"<Escalation(id={self.id}, ticket_id={self.ticket_id}, reason={self.reason})>"
