"""
Knowledge Retrieval Skill for FTE Agent.

Uses pgvector similarity search to retrieve relevant knowledge from the database.
Falls back to product_info.txt file search.
"""
import asyncio
from typing import Annotated

from pydantic import Field
from app.config import get_settings
from app.database import get_session_factory

# Import OpenAI Agents SDK with fallback for different package versions
try:
    from openai_agents import function_tool, RunContextWrapper
except ImportError:
    from agents import function_tool, RunContextWrapper


@function_tool
async def knowledge_retrieval_skill(
    ctx: RunContextWrapper,
    query: Annotated[str, Field(description="The search query to find relevant knowledge")],
    limit: Annotated[int, Field(description="Maximum number of results to return", ge=1, le=10)] = 5,
    min_similarity: Annotated[float, Field(description="Minimum similarity threshold", ge=0.0, le=1.0)] = 0.3,
) -> str:
    """
    Retrieve relevant knowledge from the knowledge base using vector similarity search.

    This skill searches the knowledge base for information relevant to the query
    using pgvector cosine similarity. It returns formatted results that the agent
    can use to answer customer questions.

    Args:
        ctx: Run context wrapper (automatically injected)
        query: The search query to find relevant knowledge
        limit: Maximum number of results to return (default: 5)
        min_similarity: Minimum similarity threshold (default: 0.3 - lowered for better recall)

    Returns:
        Formatted string with retrieved knowledge or message if no results found
    """
    from app.crud.knowledge_base import knowledge_base_crud

    try:
        # Get session factory and create a session
        session_factory = get_session_factory()
        
        async with session_factory() as session:
            # Use the knowledge_base_crud search_similar method
            # This will search DB first, then fallback to product_info.txt
            results = await knowledge_base_crud.search_similar(
                session=session,
                query=query,
                limit=limit
            )

            if not results:
                return f"No relevant knowledge found for: '{query}'"

            # Format results with FULL context
            formatted = "📚 **Knowledge Base Results (FULL CONTEXT):**\n\n"
            for result in results:
                formatted += f"### {result.get('title', 'Unknown')}\n"
                formatted += f"{result.get('content', '')}\n\n"
            
            return formatted.strip()

    except Exception as e:
        # Log error but don't expose details to agent
        print(f"Knowledge retrieval error: {e}")
        return f"Error retrieving knowledge: {str(e)}"


# Export the skill function
__all__ = ["knowledge_retrieval_skill"]
