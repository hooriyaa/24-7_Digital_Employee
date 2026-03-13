"""
Embeddings service exports.
"""
from app.services.embeddings.service import generate_embedding, generate_embeddings_batch, get_openai_client

__all__ = [
    "generate_embedding",
    "generate_embeddings_batch",
    "get_openai_client",
]
