"""
Health check schemas.
"""
from datetime import datetime
from typing import Literal, Optional

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    """Health check response model."""
    status: Literal["healthy", "unhealthy", "degraded"] = Field(
        ...,
        description="Overall health status"
    )
    timestamp: datetime = Field(
        ...,
        description="Current timestamp"
    )
    version: str = Field(
        ...,
        description="API version"
    )
    environment: str = Field(
        ...,
        description="Environment name (development, staging, production)"
    )
    database: Literal["connected", "disconnected"] = Field(
        ...,
        description="Database connection status"
    )
    database_latency_ms: Optional[float] = Field(
        default=None,
        description="Database query latency in milliseconds"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "timestamp": "2026-02-24T00:00:00.000000Z",
                "version": "1.0.0",
                "environment": "development",
                "database": "connected",
                "database_latency_ms": 45.2,
            }
        }


class DatabaseHealthResponse(BaseModel):
    """Database health check response."""
    connected: bool = Field(..., description="Whether database is connected")
    latency_ms: Optional[float] = Field(default=None, description="Query latency")
    host: Optional[str] = Field(default=None, description="Database host")
    database: Optional[str] = Field(default=None, description="Database name")
