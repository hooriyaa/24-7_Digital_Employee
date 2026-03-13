"""
Multi-Provider AI Strategy with Fallback.

Implements cost-effective provider chain:
1. Primary: Google Gemini (via OpenAI-compatible API)
2. Fallback: OpenRouter (Qwen/DeepSeek models)
3. Optional: OpenAI (if configured)
"""
import asyncio
import os
from datetime import date, datetime, timezone
from enum import Enum
from typing import Any, Optional

from app.config import get_settings

# Import OpenAI Agents SDK with fallback for different package versions
try:
    from openai_agents import Agent, ModelSettings, RunConfig, OpenAIChatCompletionsModel
    from openai import AsyncOpenAI
except ImportError:
    from agents import Agent, ModelSettings, RunConfig, OpenAIChatCompletionsModel
    from openai import AsyncOpenAI


class ProviderStatus(Enum):
    """Provider availability status."""
    ACTIVE = "active"
    RATE_LIMITED = "rate_limited"
    ERROR = "error"
    DISABLED = "disabled"


class AIProvider:
    """
    AI Provider configuration and tracking.

    Attributes:
        name: Provider identifier
        model: Model name to use
        api_key: API key for authentication
        base_url: Optional custom base URL
        priority: Provider priority (1=primary, 2=fallback, etc.)
        daily_token_limit: Maximum tokens per day
        tokens_used_today: Tokens consumed today
        last_reset: Last token counter reset
        status: Current provider status
    """

    def __init__(
        self,
        name: str,
        model: str,
        api_key: str,
        priority: int,
        base_url: Optional[str] = None,
        daily_token_limit: int = 100000,
    ):
        self.name = name
        self.model = model
        self.api_key = api_key
        self.base_url = base_url
        self.priority = priority
        self.daily_token_limit = daily_token_limit
        self.tokens_used_today = 0
        self.last_reset = date.today()
        self.status = ProviderStatus.ACTIVE if api_key else ProviderStatus.DISABLED

    def is_available(self) -> bool:
        """Check if provider is available for use."""
        # Reset counter if new day
        if self.last_reset != date.today():
            self.tokens_used_today = 0
            self.last_reset = date.today()
            self.status = ProviderStatus.ACTIVE

        if self.status != ProviderStatus.ACTIVE:
            return False

        # Check token limit
        remaining = self.daily_token_limit - self.tokens_used_today
        return remaining > 0

    def record_tokens(self, tokens: int):
        """Record token usage."""
        self.tokens_used_today += tokens

        # Check if limit exceeded
        if self.tokens_used_today >= self.daily_token_limit:
            self.status = ProviderStatus.RATE_LIMITED

    def get_remaining_tokens(self) -> int:
        """Get remaining tokens for today."""
        if self.last_reset != date.today():
            return self.daily_token_limit
        return max(0, self.daily_token_limit - self.tokens_used_today)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary for API response."""
        return {
            "name": self.name,
            "model": self.model,
            "priority": self.priority,
            "status": self.status.value,
            "tokens_used_today": self.tokens_used_today,
            "daily_limit": self.daily_token_limit,
            "remaining_tokens": self.get_remaining_tokens(),
        }


class ProviderManager:
    """
    Manages multiple AI providers with automatic fallback.

    Provider Chain:
    1. Google Gemini (primary) - via OpenAI-compatible API
    2. OpenRouter Qwen/DeepSeek (fallback)
    3. OpenAI (optional, if configured)
    """

    def __init__(self):
        """Initialize provider manager with configured providers."""
        self.settings = get_settings()
        self._providers: list[AIProvider] = []
        self._active_provider: Optional[AIProvider] = None
        self._gemini_client: Optional[AsyncOpenAI] = None
        self._gemini_model: Optional[OpenAIChatCompletionsModel] = None
        self._initialize_providers()

    def _initialize_providers(self):
        """Initialize providers from configuration."""
        # Primary: Google Gemini via OpenAI-compatible API
        # Create AsyncOpenAI client for Gemini
        gemini_api_key = self.settings.gemini_api_key
        gemini_model = self.settings.gemini_model  # Use model from settings

        self._gemini_client = AsyncOpenAI(
            api_key=gemini_api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai",
        )

        # Create model object using OpenAIChatCompletionsModel
        # Use raw model name without any prefixes
        self._gemini_model = OpenAIChatCompletionsModel(
            openai_client=self._gemini_client,
            model=gemini_model,  # Use model from settings
        )

        gemini_provider = AIProvider(
            name="gemini",
            model=gemini_model,  # Use model from settings
            api_key=gemini_api_key,
            priority=1,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai",
            daily_token_limit=self.settings.gemini_daily_token_limit,
        )
        self._providers.append(gemini_provider)

        # Fallback: OpenRouter (Qwen/DeepSeek)
        openrouter_provider = AIProvider(
            name="openrouter",
            model=f"openrouter/{self.settings.openrouter_model}",
            api_key=self.settings.openrouter_api_key,
            priority=2,
            base_url="https://openrouter.ai/api/v1",
            daily_token_limit=self.settings.openrouter_daily_token_limit,
        )
        self._providers.append(openrouter_provider)

        # Optional: OpenAI (if configured)
        if self.settings.openai_api_key:
            openai_provider = AIProvider(
                name="openai",
                model="gpt-4.1",
                api_key=self.settings.openai_api_key,
                priority=3,
                daily_token_limit=self.settings.openai_daily_token_limit,
            )
            self._providers.append(openai_provider)

        # Sort by priority
        self._providers.sort(key=lambda p: p.priority)

        # Select active provider
        self._select_active_provider()

    def _select_active_provider(self):
        """Select the first available provider."""
        for provider in self._providers:
            if provider.is_available():
                self._active_provider = provider
                return

        self._active_provider = None

    def get_active_provider(self) -> Optional[AIProvider]:
        """Get the currently active provider."""
        self._select_active_provider()
        return self._active_provider

    def get_all_providers(self) -> list[AIProvider]:
        """Get all configured providers."""
        return self._providers

    def get_provider_status(self) -> list[dict[str, Any]]:
        """Get status of all providers."""
        return [p.to_dict() for p in self._providers]

    def get_run_config(self) -> RunConfig:
        """Get RunConfig with tracing disabled."""
        return RunConfig(tracing_disabled=True)

    def create_agent(
        self,
        name: str,
        instructions: str,
        tools: Optional[list] = None,
        temperature: float = 0.7,
    ) -> Agent:
        """
        Create an agent using the active provider.

        Uses OpenAI Compatibility pattern for Gemini:
        - AsyncOpenAI client with Google's base_url
        - OpenAIChatCompletionsModel object (not string)
        - No provider argument

        Args:
            name: Agent name
            instructions: Agent instructions
            tools: Optional list of function tools
            temperature: Model temperature

        Returns:
            Configured Agent instance
        """
        provider = self.get_active_provider()

        if provider is None:
            raise RuntimeError("No AI provider available")

        # For Gemini, use the pre-created model object
        if provider.name == "gemini" and self._gemini_model is not None:
            return Agent(
                name=name,
                instructions=instructions,
                model=self._gemini_model,
                model_settings=ModelSettings(temperature=temperature),
                tools=tools or [],
            )
        else:
            # For non-Gemini providers, use model string
            return Agent(
                name=name,
                instructions=instructions,
                model=provider.model,
                model_settings=ModelSettings(temperature=temperature),
                tools=tools or [],
            )

    async def execute_with_fallback(
        self,
        func: callable,
        *args,
        **kwargs,
    ) -> Any:
        """
        Execute a function with automatic provider fallback.

        Tries each provider in priority order until one succeeds.

        Args:
            func: Async function to execute (should accept provider as kwarg)
            *args: Positional arguments for func
            **kwargs: Keyword arguments for func

        Returns:
            Result from successful provider execution

        Raises:
            RuntimeError: If all providers fail
        """
        last_error = None

        for provider in self._providers:
            if not provider.is_available():
                continue

            try:
                # Execute with current provider
                kwargs["provider"] = provider
                result = await func(*args, **kwargs)

                # Record token usage if available
                if hasattr(result, "usage") and result.usage:
                    provider.record_tokens(result.usage.total_tokens)

                return result

            except Exception as e:
                last_error = e
                print(f"Provider {provider.name} failed: {e}")

                # Mark provider as error temporarily
                provider.status = ProviderStatus.ERROR

        # All providers failed
        raise RuntimeError(f"All providers failed. Last error: {last_error}")

    def reset_all_tokens(self):
        """Reset token counters for all providers."""
        for provider in self._providers:
            provider.tokens_used_today = 0
            provider.status = ProviderStatus.ACTIVE
            provider.last_reset = date.today()


# Singleton instance
provider_manager = ProviderManager()
