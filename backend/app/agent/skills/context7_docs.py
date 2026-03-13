"""
External Documentation Search Skill using Context7 MCP.

Allows the agent to fetch technical documentation from Context7
for libraries not in the local knowledge base.
"""
from typing import Annotated

from pydantic import Field
from app.services.context7 import context7_client

# Import OpenAI Agents SDK with fallback for different package versions
try:
    from openai_agents import function_tool, RunContextWrapper
except ImportError:
    from agents import function_tool, RunContextWrapper


@function_tool
async def external_docs_search(
    ctx: RunContextWrapper,
    library: Annotated[str, Field(description="Library name (e.g., 'fastapi', 'next.js', 'openai-agents-sdk')")],
    query: Annotated[str, Field(description="Specific question or topic to search for")],
) -> str:
    """
    Search external technical documentation using Context7 MCP.
    
    Use this skill when:
    - The query is about a technical library or framework
    - The information is not in the local knowledge base
    - You need up-to-date API documentation
    - The query requires implementation details or code examples
    
    Supported libraries include:
    - FastAPI
    - OpenAI Agents SDK
    - Next.js
    - PostgreSQL
    - pgvector
    - Apache Kafka
    - And many more via Context7
    
    Args:
        ctx: Run context wrapper (automatically injected)
        library: Library name to search documentation for
        query: Specific question or topic
        
    Returns:
        Documentation content or error message if not found
    """
    try:
        # Fetch documentation from Context7
        result = await context7_client.fetch_documentation(
            library=library,
            query=query,
        )
        
        if result:
            return f"Documentation for {library}:\n\n{result}"
        else:
            return f"No documentation found for '{library}': {query}"
            
    except Exception as e:
        print(f"External docs search error: {e}")
        return f"Error fetching documentation: {str(e)}"


@function_tool
async def multi_library_search(
    ctx: RunContextWrapper,
    topic: Annotated[str, Field(description="Topic to search across multiple libraries")],
    libraries: Annotated[
        list[str],
        Field(description="List of library names to search (e.g., ['fastapi', 'openai-agents-sdk'])")
    ] = ["fastapi", "openai-agents-sdk", "next.js"],
) -> str:
    """
    Search documentation across multiple libraries for a topic.
    
    Use this skill when:
    - The query involves integration between multiple libraries
    - You need to compare approaches across libraries
    - The topic is general and could apply to multiple frameworks
    
    Args:
        ctx: Run context wrapper (automatically injected)
        topic: Topic to search for
        libraries: List of libraries to search (default: fastapi, openai-agents-sdk, next.js)
        
    Returns:
        Combined documentation results from all libraries
    """
    try:
        results = await context7_client.search_knowledge_base(
            topic=topic,
            libraries=libraries,
        )
        
        if not results:
            return f"No documentation found for topic: '{topic}'"
        
        # Format results
        formatted_results = []
        for result in results:
            formatted = f"""
## {result['library'].title()}

{result['content']}
"""
            formatted_results.append(formatted)
        
        return "\n---\n".join(formatted_results)
        
    except Exception as e:
        print(f"Multi-library search error: {e}")
        return f"Error searching documentation: {str(e)}"


# Export the skill functions
__all__ = ["external_docs_search", "multi_library_search"]
