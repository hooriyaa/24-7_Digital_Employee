"""
AI Agent module for Customer Success Digital FTE.

Provides the FTEAgent class with skills for customer support automation.
"""
from app.agent.fte_agent import FTEAgent, create_fte_agent
from app.agent.skills.knowledge_retrieval import knowledge_retrieval_skill

__all__ = [
    "FTEAgent",
    "create_fte_agent",
    "knowledge_retrieval_skill",
]
