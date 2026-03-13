"""
Test FTE Agent implementation.
"""
import asyncio

from app.agent import FTEAgent, create_fte_agent, knowledge_retrieval_skill
from app.agent.fte_agent import FTEAgentConfig


def test_agent_imports():
    """Test that all agent components can be imported."""
    print("Testing agent imports...")
    
    assert FTEAgent is not None
    assert create_fte_agent is not None
    assert knowledge_retrieval_skill is not None
    assert FTEAgentConfig is not None
    
    print("  Agent imports: PASSED")
    return True


def test_agent_config():
    """Test agent configuration."""
    print("\nTesting agent configuration...")
    
    config = FTEAgentConfig(
        model="gpt-4.1",
        temperature=0.7,
        max_tokens=2000,
        enable_knowledge_retrieval=True,
        enable_sentiment_analysis=True,
        escalation_threshold=0.7,
    )
    
    assert config.model == "gpt-4.1"
    assert config.temperature == 0.7
    assert config.enable_knowledge_retrieval is True
    
    print("  Agent configuration: PASSED")
    return config


def test_agent_creation():
    """Test FTEAgent creation."""
    print("\nTesting FTEAgent creation...")
    
    agent = create_fte_agent()
    
    assert agent is not None
    assert agent.config is not None
    assert agent.agent is not None
    
    print("  FTEAgent creation: PASSED")
    print(f"  Agent name: {agent.agent.name}")
    print(f"  Model: {agent.config.model}")
    
    return agent


def test_agent_tools():
    """Test that agent has tools configured."""
    print("\nTesting agent tools...")
    
    agent = create_fte_agent()
    
    # Check that tools are configured
    assert agent.agent.tools is not None
    assert len(agent.agent.tools) > 0
    
    print(f"  Number of tools: {len(agent.agent.tools)}")
    print("  Agent tools: PASSED")
    
    return True


async def test_knowledge_retrieval_skill():
    """Test knowledge retrieval skill (without actual DB)."""
    print("\nTesting knowledge retrieval skill structure...")
    
    # Check that the skill function exists
    assert knowledge_retrieval_skill is not None
    
    print("  Knowledge retrieval skill: PASSED")
    return True


async def main():
    """Run all agent tests."""
    print("=" * 50)
    print("FTE Agent Tests")
    print("=" * 50)
    
    try:
        # Basic tests
        test_agent_imports()
        config = test_agent_config()
        agent = test_agent_creation()
        test_agent_tools()
        
        # Async tests
        await test_knowledge_retrieval_skill()
        
        print("\n" + "=" * 50)
        print("All FTE Agent Tests PASSED!")
        print("=" * 50)
        print("\nAgent Summary:")
        print(f"  - Name: {agent.agent.name}")
        print(f"  - Model: {agent.config.model}")
        print(f"  - Tools: {len(agent.agent.tools)}")
        print(f"  - Knowledge Retrieval: {'Enabled' if agent.config.enable_knowledge_retrieval else 'Disabled'}")
        print(f"  - Sentiment Analysis: {'Enabled' if agent.config.enable_sentiment_analysis else 'Disabled'}")
        print(f"  - Escalation Threshold: {agent.config.escalation_threshold}")
        
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
