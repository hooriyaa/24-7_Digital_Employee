"""
Customer model - Unified customer identity across all channels.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

# Type alias for JSON data
JSONDict = dict

if TYPE_CHECKING:
    from app.models.ticket import Ticket
    from app.models.channel_identity import ChannelIdentity


class Customer(SQLModel, table=True):
    """
    Customer entity representing a unified identity across all channels.
    
    Attributes:
        id: UUID primary key (auto-generated)
        email: Unique email address (required)
        phone: Unique phone number (optional)
        name: Customer name (required)
        metadata: Additional customer data (JSON)
        created_at: Timestamp of creation
        updated_at: Timestamp of last update
    """
    __tablename__ = "customers"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique customer identifier"
    )
    
    email: str = Field(
        ...,
        max_length=255,
        unique=True,
        index=True,
        description="Customer email address"
    )
    
    phone: Optional[str] = Field(
        default=None,
        max_length=20,
        unique=True,
        index=True,
        description="Customer phone number"
    )
    
    name: str = Field(
        ...,
        max_length=255,
        description="Customer full name"
    )
    
    custom_metadata: dict = Field(
        default={},
        sa_type=JSON,
        description="Additional customer metadata"
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
    tickets: list["Ticket"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    
    channel_identities: list["ChannelIdentity"] = Relationship(
        back_populates="customer",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    
    def __repr__(self) -> str:
        return f"<Customer(id={self.id}, email={self.email}, name={self.name})>"
