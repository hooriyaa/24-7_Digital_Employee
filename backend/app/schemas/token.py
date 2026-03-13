"""
Token schemas for JWT authentication.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class Token(BaseModel):
    """Token response model."""
    access_token: str = Field(..., description="JWT access token")
    refresh_token: str = Field(..., description="JWT refresh token")
    token_type: str = Field(default="bearer", description="Token type")
    expires_in: int = Field(..., description="Access token expiration in seconds")


class TokenData(BaseModel):
    """Decoded token payload."""
    sub: Optional[str] = Field(default=None, description="Subject (username/email)")
    exp: Optional[datetime] = Field(default=None, description="Expiration time")
    iat: Optional[datetime] = Field(default=None, description="Issued at time")
    type: Optional[str] = Field(default=None, description="Token type (access/refresh)")
    email: Optional[str] = Field(default=None, description="User email")
    role: Optional[str] = Field(default=None, description="User role")


class RefreshTokenRequest(BaseModel):
    """Refresh token request model."""
    refresh_token: str = Field(..., description="JWT refresh token")
