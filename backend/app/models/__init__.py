"""
Database models for Customer Success Digital FTE.

All models use SQLModel with proper async relationships and pgvector support.
"""
from sqlmodel import SQLModel

# Import all models to ensure they're registered
from app.models.customer import Customer
from app.models.channel import Channel, ChannelIdentity
from app.models.conversation import Conversation
from app.models.message import Message
from app.models.ticket import Ticket
from app.models.escalation import Escalation
from app.models.ai_provider import AIProvider
from app.models.knowledge_base import KnowledgeBase

# Export all models for easy importing
__all__ = [
    "Customer",
    "Channel",
    "ChannelIdentity",
    "Conversation",
    "Message",
    "Ticket",
    "Escalation",
    "AIProvider",
    "KnowledgeBase",
]
