"""
Application configuration module.

Centralized configuration management using Pydantic Settings v2.
All environment variables are validated on startup.
Missing mandatory keys raise clear validation errors.
"""
import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Optional

from dotenv import load_dotenv
from pydantic import Field, field_validator, BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict

# Load .env file before any settings are initialized
# This ensures environment variables are available for Pydantic Settings
load_dotenv(Path(__file__).parent.parent / '.env')


class DatabaseSettings(BaseModel):
    """Database connection settings."""
    user: str = Field(..., description="PostgreSQL username")
    password: str = Field(..., description="PostgreSQL password")
    db: str = Field(..., description="PostgreSQL database name")
    host: str = Field(..., description="PostgreSQL host")
    port: int = Field(default=5432, description="PostgreSQL port")


class AppSettings(BaseSettings):
    """
    Main application settings.

    Aggregates all configuration sections and validates on startup.
    Missing mandatory keys raise clear validation errors.
    """
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent / '.env'),
        env_file_encoding='utf-8',
        case_sensitive=False,
        extra='ignore',
    )

    # Application
    app_name: str = Field(default="Customer Success Digital FTE", description="Application name")
    app_env: str = Field(default="development", description="Environment (development, staging, production)")
    debug: bool = Field(default=False, description="Enable debug mode")
    api_prefix: str = Field(default="/api/v1", description="API URL prefix")

    # Database connection URL (Neon or local PostgreSQL)
    database_url: str = Field(
        ...,
        description="PostgreSQL connection URL with sslmode for Neon"
    )

    # Database settings (POSTGRES_ prefix)
    postgres_user: str = Field(..., description="PostgreSQL username")
    postgres_password: str = Field(..., description="PostgreSQL password")
    postgres_db: str = Field(..., description="PostgreSQL database name")
    postgres_host: str = Field(..., description="PostgreSQL host")
    postgres_port: int = Field(default=5432, description="PostgreSQL port")

    # CORS
    cors_origins: str = Field(
        default="http://localhost:3000",
        description="Comma-separated list of allowed CORS origins"
    )

    # Infrastructure
    kafka_bootstrap_servers: str = Field(
        default="localhost:9092",
        description="Kafka bootstrap servers"
    )

    # Gmail settings (GMAIL_ prefix) - Optional for demo
    gmail_client_id: Optional[str] = Field(default=None, description="Gmail OAuth 2.0 Client ID")
    gmail_client_secret: Optional[str] = Field(default=None, description="Gmail OAuth 2.0 Client Secret")
    gmail_api_key: Optional[str] = Field(default=None, description="Gmail API Key")
    gmail_redirect_uri: str = Field(
        default="http://localhost:8000/webhooks/gmail/callback",
        description="OAuth 2.0 redirect URI"
    )

    # AI settings - Gemini primary, OpenRouter fallback
    gemini_api_key: str = Field(..., description="Google Gemini API Key")
    gemini_model: str = Field(default="gemini-2.0-flash", description="Gemini model name")
    openrouter_api_key: str = Field(..., description="OpenRouter API Key for Qwen/DeepSeek")
    openrouter_model: str = Field(default="qwen-2.5-coder-32b-instruct", description="OpenRouter model")
    openai_api_key: Optional[str] = Field(default=None, description="OpenAI API Key (optional)")
    gemini_daily_token_limit: int = Field(default=100000, description="Gemini daily token limit")
    openrouter_daily_token_limit: int = Field(default=100000, description="OpenRouter daily token limit")
    openai_daily_token_limit: int = Field(default=100000, description="OpenAI daily token limit")

    # Context7 settings (CONTEXT7_ prefix)
    context7_enabled: bool = Field(default=True, description="Enable Context7 MCP integration")
    context7_api_key: str = Field(..., description="Context7 API Key")

    # UltraMsg settings (ULTRAMSG_ prefix) - Optional for demo
    ultramsg_instance_id: Optional[str] = Field(default=None, description="UltraMsg instance ID")
    ultramsg_token: Optional[str] = Field(default=None, description="UltraMsg API token")

    # Security settings
    secret_key: str = Field(..., min_length=32, description="Secret key for JWT (min 32 chars)")
    algorithm: str = Field(default="HS256", description="JWT signing algorithm")
    access_token_expire_minutes: int = Field(default=15, description="Access token expiration (minutes)")
    refresh_token_expire_days: int = Field(default=7, description="Refresh token expiration (days)")

    # Kafka settings (KAFKA_ prefix)
    kafka_topic_tickets_create: str = Field(default="tickets.create", description="Tickets create topic")
    kafka_topic_tickets_update: str = Field(default="tickets.update", description="Tickets update topic")
    kafka_topic_messages_send: str = Field(default="messages.send", description="Messages send topic")
    kafka_topic_escalations_trigger: str = Field(default="escalations.trigger", description="Escalations topic")

    def export_to_environment(self):
        """
        Export API keys to environment variables for LiteLLM compatibility.
        
        LiteLLM reads from environment variables, so we need to ensure
        GEMINI_API_KEY and OPENROUTER_API_KEY are available.
        """
        os.environ["GEMINI_API_KEY"] = self.gemini_api_key
        os.environ["OPENROUTER_API_KEY"] = self.openrouter_api_key
        if self.openai_api_key:
            os.environ["OPENAI_API_KEY"] = self.openai_api_key

    @property
    def database(self) -> DatabaseSettings:
        """Get database settings as a nested object."""
        return DatabaseSettings(
            user=self.postgres_user,
            password=self.postgres_password,
            db=self.postgres_db,
            host=self.postgres_host,
            port=self.postgres_port,
        )

    @property
    def gmail(self) -> dict[str, str]:
        """Get Gmail settings as a nested object."""
        return {
            "client_id": self.gmail_client_id or "",
            "client_secret": self.gmail_client_secret or "",
            "api_key": self.gmail_api_key or "",
            "redirect_uri": self.gmail_redirect_uri,
        }

    @property
    def ai(self) -> dict[str, Any]:
        """Get AI settings as a nested object."""
        return {
            "openai_api_key": self.openai_api_key or "",
            "gemini_api_key": self.gemini_api_key,
            "openrouter_api_key": self.openrouter_api_key,
            "gemini_daily_token_limit": self.gemini_daily_token_limit,
            "openrouter_daily_token_limit": self.openrouter_daily_token_limit,
            "openai_daily_token_limit": self.openai_daily_token_limit,
        }

    @property
    def context7(self) -> dict[str, Any]:
        """Get Context7 settings as a nested object."""
        return {
            "enabled": self.context7_enabled,
            "api_key": self.context7_api_key,
        }

    @property
    def ultramsg(self) -> dict[str, str]:
        """Get UltraMsg settings as a nested object."""
        return {
            "instance_id": self.ultramsg_instance_id or "",
            "token": self.ultramsg_token or "",
        }

    @property
    def security(self) -> dict[str, Any]:
        """Get security settings as a nested object."""
        return {
            "secret_key": self.secret_key,
            "algorithm": self.algorithm,
            "access_token_expire_minutes": self.access_token_expire_minutes,
            "refresh_token_expire_days": self.refresh_token_expire_days,
        }

    @property
    def kafka(self) -> dict[str, str]:
        """Get Kafka settings as a nested object."""
        return {
            "bootstrap_servers": self.kafka_bootstrap_servers,
            "topic_tickets_create": self.kafka_topic_tickets_create,
            "topic_tickets_update": self.kafka_topic_tickets_update,
            "topic_messages_send": self.kafka_topic_messages_send,
            "topic_escalations_trigger": self.kafka_topic_escalations_trigger,
        }

    @field_validator('database_url')
    @classmethod
    def validate_database_url(cls, v: str) -> str:
        """Validate database URL is not empty and contains required components."""
        if not v or not v.strip():
            raise ValueError("DATABASE_URL cannot be empty")
        if not v.startswith('postgresql://') and not v.startswith('postgresql+asyncpg://'):
            raise ValueError(
                "DATABASE_URL must start with 'postgresql://' or 'postgresql+asyncpg://'. "
                "For Neon: use 'postgresql://user:pass@host/db?sslmode=require'"
            )
        return v

    @field_validator('cors_origins')
    @classmethod
    def parse_cors_origins(cls, v: str) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        if not v:
            return []
        return [origin.strip() for origin in v.split(',')]

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.app_env.lower() == 'production'

    @property
    def is_development(self) -> bool:
        """Check if running in development environment."""
        return self.app_env.lower() == 'development'


@lru_cache
def get_settings() -> AppSettings:
    """
    Get cached application settings.

    Uses LRU cache to avoid re-reading environment variables on each call.
    Settings are validated on first call and cached thereafter.

    Returns:
        AppSettings: Validated application settings

    Raises:
        pydantic.ValidationError: If any mandatory environment variable is missing
    """
    settings = AppSettings()
    # Export API keys to environment for LiteLLM compatibility
    settings.export_to_environment()
    return settings


# Global settings instance (lazy-loaded)
_settings: AppSettings | None = None


def get_settings_instance() -> AppSettings:
    """
    Get or create the global settings instance.

    Returns:
        AppSettings: Application settings instance
    """
    global _settings
    if _settings is None:
        _settings = get_settings()
    return _settings
