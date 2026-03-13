"""
Skills module for AI agents.

Each skill is a function tool that the agent can use to perform specific tasks.
"""
from app.agent.skills.knowledge_retrieval import knowledge_retrieval_skill
from app.agent.skills.context7_docs import external_docs_search, multi_library_search

__all__ = [
    "knowledge_retrieval_skill",
    "external_docs_search",
    "multi_library_search",
]
