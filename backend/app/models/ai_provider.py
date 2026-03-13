"""
AIProvider model - AI provider configuration and quota tracking.
"""
from datetime import date, datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class AIProvider(SQLModel, table=True):
    """
    AIProvider entity for tracking AI provider configuration and usage.
    
    Attributes:
        id: Primary key
        name: Provider name (openai, gemini, qwen)
        priority: Provider priority (1=primary, 2=fallback, 3=secondary fallback)
        is_active: Whether provider is active
        daily_token_limit: Daily token usage limit
        tokens_used_today: Tokens used today
        last_reset: Last token reset date
    """
    __tablename__ = "ai_providers"
    
    id: int = Field(
        default=None,
        primary_key=True,
        description="Provider identifier"
    )
    
    name: str = Field(
        ...,
        max_length=50,
        unique=True,
        index=True,
        description="Provider name (openai, gemini, qwen)"
    )
    
    priority: int = Field(
        ...,
        ge=1,
        le=3,
        index=True,
        description="Provider priority (1=primary, 2=fallback, 3=secondary fallback)"
    )
    
    is_active: bool = Field(
        default=True,
        index=True,
        description="Whether provider is active"
    )
    
    daily_token_limit: int = Field(
        default=100000,
        ge=0,
        description="Daily token usage limit"
    )
    
    tokens_used_today: int = Field(
        default=0,
        ge=0,
        description="Tokens used today"
    )
    
    last_reset: date = Field(
        default_factory=date.today,
        description="Last token reset date"
    )
    
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record creation timestamp"
    )
    
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Record last update timestamp"
    )
    
    def __repr__(self) -> str:
        return f"<AIProvider(id={self.id}, name={self.name}, priority={self.priority})>"
