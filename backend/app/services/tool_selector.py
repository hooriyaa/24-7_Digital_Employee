"""
Tool Selector Service.

Helps the FTE Agent automatically choose the right tool for each query.
"""
from enum import Enum
from typing import Optional


class ToolType(str, Enum):
    """Available tool types for the agent."""
    
    KNOWLEDGE_RETRIEVAL = "knowledge_retrieval"
    EXTERNAL_DOCS = "external_docs"
    CRM_LOOKUP = "crm_lookup"
    TICKET_MANAGEMENT = "ticket_management"
    GENERAL_CHAT = "general_chat"


class ToolSelector:
    """
    Service for selecting the appropriate tool based on query intent.
    
    Analyzes query patterns to determine which tool should be used:
    - Knowledge Retrieval: Internal knowledge base queries
    - External Docs: Technical documentation (FastAPI, Next.js, etc.)
    - CRM Lookup: Customer information queries
    - Ticket Management: Ticket operations
    - General Chat: Casual conversation
    """
    
    # Keywords that indicate knowledge base queries
    KNOWLEDGE_KEYWORDS = [
        "how do i",
        "what is",
        "explain",
        "guide",
        "tutorial",
        "steps",
        "process",
        "policy",
        "procedure",
    ]
    
    # Keywords that indicate technical documentation queries
    TECH_KEYWORDS = [
        "api",
        "endpoint",
        "sdk",
        "library",
        "framework",
        "fastapi",
        "nextjs",
        "next.js",
        "typescript",
        "python",
        "database",
        "postgresql",
        "kafka",
        "integration",
        "implementation",
        "code example",
        "sample code",
    ]
    
    # Keywords that indicate CRM/customer queries
    CRM_KEYWORDS = [
        "customer",
        "account",
        "profile",
        "email",
        "phone",
        "contact",
        "user",
        "client",
    ]
    
    # Keywords that indicate ticket operations
    TICKET_KEYWORDS = [
        "ticket",
        "case",
        "issue",
        "problem",
        "status",
        "update",
        "close",
        "reopen",
        "assign",
        "priority",
    ]
    
    def select_tool(self, query: str) -> ToolType:
        """
        Select the appropriate tool for a query.
        
        Args:
            query: User query text
            
        Returns:
            ToolType enum value
        """
        query_lower = query.lower()
        
        # Score each tool type
        scores = {
            ToolType.KNOWLEDGE_RETRIEVAL: 0,
            ToolType.EXTERNAL_DOCS: 0,
            ToolType.CRM_LOOKUP: 0,
            ToolType.TICKET_MANAGEMENT: 0,
        }
        
        # Score knowledge retrieval
        for keyword in self.KNOWLEDGE_KEYWORDS:
            if keyword in query_lower:
                scores[ToolType.KNOWLEDGE_RETRIEVAL] += 2
        
        # Score external docs
        for keyword in self.TECH_KEYWORDS:
            if keyword in query_lower:
                scores[ToolType.EXTERNAL_DOCS] += 2
        
        # Score CRM lookup
        for keyword in self.CRM_KEYWORDS:
            if keyword in query_lower:
                scores[ToolType.CRM_LOOKUP] += 2
        
        # Score ticket management
        for keyword in self.TICKET_KEYWORDS:
            if keyword in query_lower:
                scores[ToolType.TICKET_MANAGEMENT] += 2
        
        # Find highest scoring tool
        max_score = max(scores.values())
        
        if max_score == 0:
            return ToolType.GENERAL_CHAT
        
        # Get all tools with max score
        top_tools = [tool for tool, score in scores.items() if score == max_score]
        
        # Priority order for ties
        priority = [
            ToolType.TICKET_MANAGEMENT,
            ToolType.CRM_LOOKUP,
            ToolType.EXTERNAL_DOCS,
            ToolType.KNOWLEDGE_RETRIEVAL,
        ]
        
        for tool in priority:
            if tool in top_tools:
                return tool
        
        return top_tools[0]
    
    def get_tool_description(self, tool_type: ToolType) -> str:
        """
        Get human-readable description of tool choice.
        
        Args:
            tool_type: Selected tool type
            
        Returns:
            Description string
        """
        descriptions = {
            ToolType.KNOWLEDGE_RETRIEVAL: "Searching internal knowledge base",
            ToolType.EXTERNAL_DOCS: "Fetching technical documentation",
            ToolType.CRM_LOOKUP: "Looking up customer information",
            ToolType.TICKET_MANAGEMENT: "Managing ticket operations",
            ToolType.GENERAL_CHAT: "General conversation",
        }
        return descriptions.get(tool_type, "Unknown tool")


# Singleton instance
tool_selector = ToolSelector()
