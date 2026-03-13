"""
Search Knowledge Base Skill for FTE Agent.

Reads from local product_info.txt file to provide Smart Jawab.
"""
import os
from pathlib import Path
from typing import Annotated

from pydantic import Field

# Import OpenAI Agents SDK with fallback for different package versions
try:
    from openai_agents import function_tool, RunContextWrapper
except ImportError:
    from agents import function_tool, RunContextWrapper


# Path to product info file
PRODUCT_INFO_PATH = Path(__file__).parent.parent / "data" / "docs" / "product_info.txt"


@function_tool
async def search_knowledge_base(
    ctx: RunContextWrapper,
    query: Annotated[str, Field(description="The search query to find relevant product information")],
) -> str:
    """
    Search the local knowledge base (product_info.txt) for relevant information.

    This skill reads from the product_info.txt file and returns relevant sections
    that match the query. Use this for product information, pricing, features,
    common issues, and contact information.

    Args:
        ctx: Run context wrapper (automatically injected)
        query: The search query to find relevant product information

    Returns:
        Formatted string with retrieved knowledge or message if not found
    """
    try:
        # Check if file exists
        if not PRODUCT_INFO_PATH.exists():
            return "Knowledge base file not found. Please ensure product_info.txt exists."

        # Read the file
        with open(PRODUCT_INFO_PATH, "r", encoding="utf-8") as f:
            content = f.read()

        # Split into sections
        sections = content.split("## ")

        # Search for relevant sections with FLEXIBLE matching
        relevant_sections = []
        query_lower = query.lower()
        query_keywords = [word for word in query_lower.split() if len(word) > 2]

        for section in sections:
            if not section.strip():
                continue

            # Check if query terms appear in section
            section_lower = section.lower()

            # Flexible keyword matching - ANY keyword match includes the section
            matches = sum(1 for term in query_keywords if term in section_lower)

            if matches > 0:
                relevant_sections.append((matches, section))

        # Sort by relevance
        relevant_sections.sort(key=lambda x: x[0], reverse=True)

        # Return top matches with FULL content
        if relevant_sections:
            result = "📚 **Knowledge Base Results (FULL CONTEXT):**\n\n"
            for _, section in relevant_sections[:5]:  # Top 5 sections with FULL content
                result += f"## {section}\n\n"
            return result.strip()

        # If no specific matches, return the FULL content
        return f"📖 **Full Product Information (FULL CONTEXT):**\n\n{content}"

    except Exception as e:
        # Log error but don't expose details to agent
        print(f"Knowledge base search error: {e}")
        return f"Error searching knowledge base: {str(e)}"


# Export the skill function
__all__ = ["search_knowledge_base"]
