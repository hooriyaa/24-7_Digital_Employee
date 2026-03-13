"""
Embeddings service for generating vector embeddings.

Uses OpenAI's text-embedding-ada-002 model for consistent embeddings.
"""
from typing import Optional

from openai import AsyncOpenAI

from app.config import get_settings

_settings = get_settings()

# Initialize OpenAI client for embeddings
_openai_client: Optional[AsyncOpenAI] = None


def get_openai_client() -> AsyncOpenAI:
    """Get or create OpenAI client for embeddings."""
    global _openai_client
    if _openai_client is None:
        _openai_client = AsyncOpenAI(api_key=_settings.openai_api_key)
    return _openai_client


async def generate_embedding(text: str) -> Optional[list[float]]:
    """
    Generate embedding vector for text using OpenAI.
    
    Args:
        text: Text to embed
        
    Returns:
        List of floats (1536 dimensions for text-embedding-ada-002)
        or None if generation fails
    """
    try:
        client = get_openai_client()
        
        response = await client.embeddings.create(
            model="text-embedding-ada-002",
            input=text,
        )
        
        return response.data[0].embedding
        
    except Exception as e:
        print(f"Embedding generation error: {e}")
        return None


async def generate_embeddings_batch(texts: list[str]) -> list[list[float]]:
    """
    Generate embeddings for multiple texts in batch.
    
    Args:
        texts: List of texts to embed
        
    Returns:
        List of embedding vectors
    """
    try:
        client = get_openai_client()
        
        response = await client.embeddings.create(
            model="text-embedding-ada-002",
            input=texts,
        )
        
        # Sort by index to maintain order
        sorted_data = sorted(response.data, key=lambda x: x.index)
        return [item.embedding for item in sorted_data]
        
    except Exception as e:
        print(f"Batch embedding error: {e}")
        return []
