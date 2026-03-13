"""
User schemas for authentication.
"""
import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    """Base user model."""
    email: EmailStr = Field(..., description="User email address")
    name: Optional[str] = Field(default=None, description="User full name")
    role: str = Field(default="agent", description="User role (agent, admin)")


class UserCreate(UserBase):
    """User creation model."""
    password: str = Field(..., min_length=8, max_length=100, description="User password")


class UserUpdate(BaseModel):
    """User update model."""
    email: Optional[EmailStr] = Field(default=None, description="User email address")
    name: Optional[str] = Field(default=None, description="User full name")
    password: Optional[str] = Field(default=None, min_length=8, max_length=100, description="New password")
    role: Optional[str] = Field(default=None, description="User role")
    is_active: Optional[bool] = Field(default=None, description="Whether user is active")


class UserResponse(UserBase):
    """User response model."""
    id: uuid.UUID = Field(..., description="User ID")
    created_at: datetime = Field(..., description="Account creation time")
    updated_at: datetime = Field(..., description="Last update time")
    is_active: bool = Field(default=True, description="Whether user is active")
    
    class Config:
        from_attributes = True


class UserInDB(UserResponse):
    """User model with hashed password (internal use)."""
    hashed_password: str = Field(..., description="Hashed password")


class LoginRequest(BaseModel):
    """Login request model."""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")
    remember_me: bool = Field(default=False, description="Extend token expiration")
