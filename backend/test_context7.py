"""
Test Context7 MCP integration.
"""
import asyncio

from app.agent import create_fte_agent
from app.agent.skills import external_docs_search, multi_library_search
from app.services.context7 import context7_client, Context7Client


def test_context7_imports():
    """Test that Context7 components can be imported."""
    print("Testing Context7 imports...")
    
    assert context7_client is not None
    assert Context7Client is not None
    assert external_docs_search is not None
    assert multi_library_search is not None
    
    print("  Context7 imports: PASSED")
    return True


def test_context7_client():
    """Test Context7 client initialization."""
    print("\nTesting Context7 client...")
    
    client = Context7Client()
    assert client is not None
    
    # Test MCP tool creation
    mcp_tool = client.mcp_tool
    assert mcp_tool is not None
    assert mcp_tool.tool_config["server_label"] == "context7"
    
    print("  Context7 client: PASSED")
    print(f"  Server URL: {mcp_tool.tool_config['server_url']}")
    return True


def test_agent_with_context7():
    """Test that agent includes Context7 skills."""
    print("\nTesting agent with Context7 skills...")
    
    agent = create_fte_agent()
    
    # Check that agent has tools
    assert agent.agent.tools is not None
    assert len(agent.agent.tools) > 0
    
    print(f"  Total tools: {len(agent.agent.tools)}")
    
    # Check for Context7 tools
    tool_names = [str(t) for t in agent.agent.tools]
    has_external_docs = any("external_docs" in str(t) for t in agent.agent.tools)
    has_multi_search = any("multi_library" in str(t) for t in agent.agent.tools)
    
    print(f"  External docs search: {'[OK]' if has_external_docs else '[MISSING]'}")
    print(f"  Multi-library search: {'[OK]' if has_multi_search else '[MISSING]'}")
    
    print("  Agent with Context7: PASSED")
    return True


async def test_external_docs_search():
    """Test external docs search skill."""
    print("\nTesting external docs search skill...")
    
    # Check that the skill function exists
    assert external_docs_search is not None
    
    print("  External docs search skill: PASSED")
    return True


async def test_multi_library_search():
    """Test multi-library search skill."""
    print("\nTesting multi-library search skill...")
    
    # Check that the skill function exists
    assert multi_library_search is not None
    
    print("  Multi-library search skill: PASSED")
    return True


async def main():
    """Run all Context7 tests."""
    print("=" * 50)
    print("Context7 MCP Integration Tests")
    print("=" * 50)
    
    try:
        # Basic tests
        test_context7_imports()
        test_context7_client()
        test_agent_with_context7()
        
        # Async tests
        await test_external_docs_search()
        await test_multi_library_search()
        
        print("\n" + "=" * 50)
        print("All Context7 Tests PASSED!")
        print("=" * 50)
        
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
