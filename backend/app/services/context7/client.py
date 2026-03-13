"""
Context7 MCP Client for documentation retrieval.

Provides RAG knowledge retrieval from Context7's documentation database.
"""
import asyncio
from typing import Any, Optional

from app.config import get_settings

_settings = get_settings()

# Import OpenAI Agents SDK with fallback for different package versions
try:
    from openai_agents import HostedMCPTool
except ImportError:
    from agents import HostedMCPTool


class Context7Client:
    """
    Context7 MCP client for fetching technical documentation.
    
    Uses OpenAI's HostedMCPTool to connect to Context7's documentation server.
    This allows the agent to fetch up-to-date documentation for any library
    that Context7 supports.
    """
    
    def __init__(self):
        """Initialize Context7 client."""
        self._mcp_tool: Optional[HostedMCPTool] = None
        self._cache: dict[str, Any] = {}
        self._cache_ttl: int = 3600  # 1 hour cache
    
    @property
    def mcp_tool(self) -> HostedMCPTool:
        """Get or create the Context7 MCP tool."""
        if self._mcp_tool is None:
            self._mcp_tool = HostedMCPTool(
                tool_config={
                    "type": "mcp",
                    "server_label": "context7",
                    "server_url": "https://mcp.context7.com/mcp",
                    "require_approval": "never",
                }
            )
        return self._mcp_tool
    
    def get_tools(self) -> list[HostedMCPTool]:
        """
        Get Context7 MCP tools for agent.
        
        Returns:
            List of MCP tools for documentation search
        """
        return [self.mcp_tool]
    
    async def fetch_documentation(
        self,
        library: str,
        query: str,
    ) -> Optional[str]:
        """
        Fetch documentation for a specific library and query.
        
        Args:
            library: Library name (e.g., "fastapi", "next.js")
            query: Specific query or topic
            
        Returns:
            Documentation content or None if not found
        """
        cache_key = f"{library}:{query}"
        
        # Check cache first
        if cache_key in self._cache:
            return self._cache[cache_key]
        
        try:
            # In production, this would call the MCP tool
            # For now, return a placeholder
            result = f"Context7 documentation for {library}: {query}"
            
            # Cache the result
            self._cache[cache_key] = result
            
            return result
            
        except Exception as e:
            print(f"Context7 fetch error: {e}")
            return None
    
    async def search_knowledge_base(
        self,
        topic: str,
        libraries: Optional[list[str]] = None,
    ) -> list[dict[str, Any]]:
        """
        Search Context7 knowledge base for a topic.
        
        Args:
            topic: Topic to search for
            libraries: Optional list of libraries to search
            
        Returns:
            List of documentation results
        """
        if libraries is None:
            libraries = ["fastapi", "openai-agents-sdk", "next.js"]
        
        results = []
        
        for library in libraries:
            doc = await self.fetch_documentation(library, topic)
            if doc:
                results.append({
                    "library": library,
                    "topic": topic,
                    "content": doc,
                })
        
        return results
    
    def clear_cache(self):
        """Clear the documentation cache."""
        self._cache.clear()


# Singleton instance
context7_client = Context7Client()
