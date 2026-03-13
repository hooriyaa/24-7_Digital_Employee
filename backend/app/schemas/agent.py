"""
Agent API schemas.
"""
import uuid
from typing import Optional

from pydantic import BaseModel, Field


class AgentRequest(BaseModel):
    """Request to generate AI response or create a ticket."""

    # For ticket creation
    customer_id: Optional[uuid.UUID] = Field(
        default=None,
        description="Customer ID (optional, will create if not provided)"
    )
    customer_name: Optional[str] = Field(
        default=None,
        description="Customer name"
    )
    customer_email: Optional[str] = Field(
        default=None,
        description="Customer email"
    )
    customer_phone: Optional[str] = Field(
        default=None,
        description="Customer phone number"
    )
    subject: str = Field(
        ...,
        description="Ticket subject (required)"
    )
    message: Optional[str] = Field(
        default=None,
        description="Initial message content"
    )
    channel: Optional[str] = Field(
        default="web",
        description="Communication channel (web, whatsapp, email)"
    )
    priority: Optional[str] = Field(
        default="normal",
        description="Ticket priority (low, normal, high, urgent)"
    )

    # For AI response generation
    ticket_id: Optional[uuid.UUID] = Field(
        default=None,
        description="Ticket ID to respond to"
    )
    force_provider: Optional[str] = Field(
        default=None,
        description="Force specific provider (gemini, openrouter)",
    )


class AgentResponse(BaseModel):
    """AI response with metadata."""

    response: str = Field(..., description="Generated response text")
    provider: str = Field(..., description="Provider used (gemini, openrouter)")
    confidence_score: float = Field(..., description="AI confidence (0.0 to 1.0)")
    sentiment_score: float = Field(..., description="Customer sentiment (-1.0 to 1.0)")
    requires_escalation: bool = Field(..., description="Whether escalation is needed")
    escalation_reason: Optional[str] = Field(default=None, description="Escalation reason")
    tokens_used: int = Field(default=0, description="Tokens consumed")


class AgentStatus(BaseModel):
    """Agent service status."""

    status: str = Field(..., description="Service status")
    active_provider: str = Field(..., description="Currently active provider")
    available_providers: list[str] = Field(..., description="All available providers")
