"""
Agent Memory Service.

Handles conversation history retrieval and context management for the FTE Agent.
"""
import uuid
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.conversation import Conversation
from app.models.message import Message
from app.models.ticket import Ticket


class AgentMemoryService:
    """
    Service for managing agent memory and conversation context.
    
    Provides methods to:
    - Retrieve conversation history
    - Get customer context
    - Build prompt context from ticket data
    """
    
    def __init__(self, db: AsyncSession):
        """
        Initialize memory service.
        
        Args:
            db: Async database session
        """
        self.db = db
    
    async def get_conversation_history(
        self,
        conversation_id: uuid.UUID,
        limit: int = 10,
    ) -> list[dict]:
        """
        Get recent conversation history.
        
        Args:
            conversation_id: Conversation UUID
            limit: Number of messages to retrieve
            
        Returns:
            List of messages with role and content
        """
        query = (
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.desc())
            .limit(limit)
        )
        
        result = await self.db.exec(query)
        messages = result.all()
        
        # Reverse to get chronological order
        messages = list(reversed(messages))
        
        return [
            {
                "role": msg.role,
                "content": msg.content,
                "sender_type": msg.sender_type,
                "created_at": msg.created_at.isoformat(),
            }
            for msg in messages
        ]
    
    async def get_customer_context(
        self,
        customer_id: uuid.UUID,
    ) -> dict:
        """
        Get customer context for personalization.
        
        Args:
            customer_id: Customer UUID
            
        Returns:
            Customer context dictionary
        """
        from app.crud.customer import customer_crud
        
        customer = await customer_crud.get(self.db, id=customer_id)
        
        if not customer:
            return {}
        
        return {
            "customer_id": str(customer.id),
            "name": customer.name,
            "email": customer.email,
        }
    
    async def get_ticket_context(
        self,
        ticket_id: uuid.UUID,
    ) -> dict:
        """
        Get full ticket context including conversation.
        
        Args:
            ticket_id: Ticket UUID
            
        Returns:
            Complete ticket context
        """
        from app.crud.ticket import ticket_crud
        
        ticket = await ticket_crud.get(self.db, id=ticket_id)
        
        if not ticket:
            return {}
        
        context = {
            "ticket_id": str(ticket.id),
            "status": ticket.status,
            "priority": ticket.priority,
            "subject": ticket.subject,
            "sentiment_score": ticket.sentiment_score,
            "confidence_score": ticket.confidence_score,
        }
        
        # Get customer context
        if ticket.customer_id:
            customer_ctx = await self.get_customer_context(ticket.customer_id)
            context.update(customer_ctx)
        
        # Get conversation history
        if ticket.conversation_id:
            history = await self.get_conversation_history(ticket.conversation_id)
            context["conversation_history"] = history
        
        return context
    
    async def build_agent_context(
        self,
        ticket_id: uuid.UUID,
    ) -> str:
        """
        Build formatted context string for agent prompt.
        
        Args:
            ticket_id: Ticket UUID
            
        Returns:
            Formatted context string
        """
        context = await self.get_ticket_context(ticket_id)
        
        if not context:
            return "No context available."
        
        # Format context for prompt
        lines = [
            "### Ticket Context",
            f"- **ID**: {context.get('ticket_id', 'N/A')}",
            f"- **Status**: {context.get('status', 'N/A')}",
            f"- **Priority**: {context.get('priority', 'N/A')}",
            f"- **Subject**: {context.get('subject', 'N/A') or 'No subject'}",
        ]
        
        if context.get('name'):
            lines.append(f"- **Customer**: {context['name']} ({context['email']})")
        
        if context.get('sentiment_score') is not None:
            lines.append(f"- **Sentiment**: {context['sentiment_score']:.2f}")
        
        if context.get('conversation_history'):
            lines.append("\n### Recent Messages")
            for msg in context['conversation_history'][-5:]:
                sender = "Customer" if msg['sender_type'] == 'customer' else "Agent"
                lines.append(f"- **{sender}**: {msg['content'][:100]}...")
        
        return "\n".join(lines)


# Factory function
def create_memory_service(db: AsyncSession) -> AgentMemoryService:
    """
    Create agent memory service instance.
    
    Args:
        db: Async database session
        
    Returns:
        AgentMemoryService instance
    """
    return AgentMemoryService(db)
