"""
Test Multi-Provider Strategy.
"""
import asyncio

from app.agent.providers import provider_manager, AIProvider, ProviderStatus
from app.agent import create_fte_agent


def test_provider_manager_init():
    """Test provider manager initialization."""
    print("Testing provider manager initialization...")
    
    assert provider_manager is not None
    assert len(provider_manager.get_all_providers()) >= 2  # Gemini + OpenRouter
    
    print("  Provider manager: PASSED")
    return True


def test_provider_status():
    """Test provider status endpoint."""
    print("\nTesting provider status...")
    
    status = provider_manager.get_provider_status()
    
    assert len(status) >= 2
    
    for provider in status:
        assert "name" in provider
        assert "priority" in provider
        assert "status" in provider
        assert "tokens_used_today" in provider
        assert "daily_limit" in provider
        assert "remaining_tokens" in provider
        
        print(f"  {provider['name']}: {provider['status']} (Priority: {provider['priority']})")
    
    # Verify Gemini is primary (priority 1)
    gemini = next((p for p in status if p["name"] == "gemini"), None)
    assert gemini is not None
    assert gemini["priority"] == 1
    
    print("  Provider status: PASSED")
    return True


def test_active_provider():
    """Test active provider selection."""
    print("\nTesting active provider selection...")
    
    active = provider_manager.get_active_provider()
    
    assert active is not None
    assert active.priority == 1  # Should be Gemini (primary)
    assert active.name == "gemini"
    
    print(f"  Active provider: {active.name} (Priority: {active.priority})")
    print("  Active provider selection: PASSED")
    return True


def test_token_tracking():
    """Test token tracking functionality."""
    print("\nTesting token tracking...")
    
    provider = provider_manager.get_active_provider()
    
    initial_tokens = provider.tokens_used_today
    
    # Record some tokens
    provider.record_tokens(1000)
    
    assert provider.tokens_used_today == initial_tokens + 1000
    
    # Check remaining
    remaining = provider.get_remaining_tokens()
    assert remaining == provider.daily_token_limit - provider.tokens_used_today
    
    # Reset
    provider.tokens_used_today = initial_tokens
    
    print("  Token tracking: PASSED")
    return True


def test_agent_creation():
    """Test agent creation with provider manager."""
    print("\nTesting agent creation...")
    
    agent = create_fte_agent()
    
    assert agent is not None
    assert agent.agent is not None
    
    # Check that agent uses LiteLLM model (Gemini)
    assert "litellm/gemini" in agent.agent.model
    
    print(f"  Agent model: {agent.agent.model}")
    print(f"  Number of tools: {len(agent.agent.tools)}")
    print("  Agent creation: PASSED")
    return True


def test_fallback_chain():
    """Test fallback chain configuration."""
    print("\nTesting fallback chain...")
    
    providers = provider_manager.get_all_providers()
    
    # Verify order
    assert providers[0].name == "gemini"
    assert providers[0].priority == 1
    
    assert providers[1].name == "openrouter"
    assert providers[1].priority == 2
    
    print("  Fallback chain: Gemini -> OpenRouter")
    print("  Fallback chain: PASSED")
    return True


async def main():
    """Run all provider tests."""
    print("=" * 50)
    print("Multi-Provider Strategy Tests")
    print("=" * 50)
    
    try:
        test_provider_manager_init()
        test_provider_status()
        test_active_provider()
        test_token_tracking()
        test_agent_creation()
        test_fallback_chain()
        
        print("\n" + "=" * 50)
        print("All Multi-Provider Tests PASSED!")
        print("=" * 50)
        
        # Print summary
        print("\nProvider Summary:")
        for provider in provider_manager.get_provider_status():
            print(f"  {provider['name']}:")
            print(f"    - Model: {provider['name']}")
            print(f"    - Priority: {provider['priority']}")
            print(f"    - Status: {provider['status']}")
            print(f"    - Remaining: {provider['remaining_tokens']:,} tokens")
        
        return True
        
    except Exception as e:
        print(f"\nTest FAILED: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
