"""
Channel and ChannelIdentity models - Communication channel types and customer channel mappings.
"""
import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON
from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from app.models.customer import Customer


class Channel(SQLModel, table=True):
    """
    Channel entity representing communication channel types.
    
    Pre-populated with: gmail, whatsapp, web
    """
    __tablename__ = "channels"
    
    id: int = Field(
        default=None,
        primary_key=True,
        description="Channel identifier"
    )
    
    name: str = Field(
        ...,
        max_length=50,
        unique=True,
        index=True,
        description="Channel name (gmail, whatsapp, web)"
    )
    
    description: Optional[str] = Field(
        default=None,
        max_length=500,
        description="Channel description"
    )
    
    is_active: bool = Field(
        default=True,
        description="Whether channel is active"
    )
    
    # Relationships
    identities: list["ChannelIdentity"] = Relationship(
        back_populates="channel",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )
    
    def __repr__(self) -> str:
        return f"<Channel(id={self.id}, name={self.name})>"


class ChannelIdentity(SQLModel, table=True):
    """
    ChannelIdentity entity linking customers to channel-specific identifiers.
    
    Enables cross-channel identity resolution.
    """
    __tablename__ = "channel_identities"
    
    id: uuid.UUID = Field(
        default_factory=uuid.uuid4,
        primary_key=True,
        description="Unique channel identity identifier"
    )
    
    customer_id: uuid.UUID = Field(
        ...,
        foreign_key="customers.id",
        ondelete="CASCADE",
        index=True,
        description="Reference to customer"
    )
    
    channel_id: int = Field(
        ...,
        foreign_key="channels.id",
        ondelete="CASCADE",
        index=True,
        description="Reference to channel"
    )
    
    channel_identifier: str = Field(
        ...,
        max_length=255,
        index=True,
        description="Channel-specific identifier (email, phone, etc.)"
    )
    
    custom_metadata: dict = Field(
        default={},
        sa_type=JSON,
        description="Channel-specific metadata"
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
    customer: "Customer" = Relationship(back_populates="channel_identities")
    channel: "Channel" = Relationship(back_populates="identities")
    
    def __repr__(self) -> str:
        return f"<ChannelIdentity(customer_id={self.customer_id}, channel={self.channel_id})>"
