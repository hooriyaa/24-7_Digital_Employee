"""
Ticket CRUD operations.
"""
import uuid
from datetime import datetime, timezone
from typing import Any

from pydantic import BaseModel, Field
from sqlmodel.ext.asyncio.session import AsyncSession

from app.crud.base import CRUDBase
from app.models.ticket import Ticket


class TicketCreate(BaseModel):
    """Ticket creation schema."""
    customer_id: uuid.UUID = Field(..., description="Customer ID")
    conversation_id: uuid.UUID = Field(..., description="Conversation ID")
    status: str = Field(default="open", description="Ticket status")
    priority: str = Field(default="normal", description="Priority level")
    subject: str | None = Field(default=None, description="Ticket subject")
    sentiment_score: float | None = Field(default=None, description="Sentiment score")
    confidence_score: float | None = Field(default=None, description="Confidence score")


class TicketUpdate(BaseModel):
    """Ticket update schema."""
    status: str | None = Field(default=None, description="Ticket status")
    priority: str | None = Field(default=None, description="Priority level")
    assigned_to: str | None = Field(default=None, description="Assigned agent")
    sentiment_score: float | None = Field(default=None, description="Sentiment score")
    confidence_score: float | None = Field(default=None, description="Confidence score")


class CRUDTicket(CRUDBase[Ticket, TicketCreate, TicketUpdate]):
    """
    Ticket CRUD operations.
    
    Extends base CRUD with ticket-specific methods.
    """
    
    async def get_open_tickets(
        self,
        session: AsyncSession,
        customer_id: uuid.UUID | None = None
    ) -> list[Ticket]:
        """
        Get all open tickets, optionally filtered by customer.
        
        Args:
            session: Async database session
            customer_id: Optional customer ID filter
            
        Returns:
            List of open tickets
        """
        filters = {"status": "open"}
        if customer_id:
            filters["customer_id"] = customer_id
        
        return await self.get_multi(session, filters=filters, limit=100)
    
    async def get_escalated_tickets(
        self,
        session: AsyncSession
    ) -> list[Ticket]:
        """
        Get all escalated tickets.
        
        Args:
            session: Async database session
            
        Returns:
            List of escalated tickets
        """
        return await self.get_multi(session, filters={"status": "escalated"}, limit=100)
    
    async def close_ticket(
        self,
        session: AsyncSession,
        *,
        ticket_id: uuid.UUID
    ) -> Ticket | None:
        """
        Close a ticket.
        
        Args:
            session: Async database session
            ticket_id: Ticket ID
            
        Returns:
            Updated ticket or None if not found
        """
        return await self.update_by_id(
            session,
            id=ticket_id,
            obj_in=TicketUpdate(
                status="closed",
            ),
        )
    
    async def assign_ticket(
        self,
        session: AsyncSession,
        *,
        ticket_id: uuid.UUID,
        agent_email: str
    ) -> Ticket | None:
        """
        Assign a ticket to an agent.

        Args:
            session: Async database session
            ticket_id: Ticket ID
            agent_email: Agent email

        Returns:
            Updated ticket or None if not found
        """
        return await self.update_by_id(
            session,
            id=ticket_id,
            obj_in=TicketUpdate(
                assigned_to=agent_email,
                status="in_progress",
            ),
        )

    async def delete_ticket_with_messages(
        self,
        session: AsyncSession,
        *,
        ticket_id: uuid.UUID
    ) -> bool:
        """
        Delete a ticket and its associated messages.

        Args:
            session: Async database session
            ticket_id: Ticket ID to delete

        Returns:
            True if deleted, False if ticket not found
        """
        from app.crud import message_crud, conversation_crud
        
        # Get the ticket
        ticket = await self.get(session, id=ticket_id)
        if not ticket:
            return False
        
        # Get the conversation
        if ticket.conversation_id:
            # Delete all messages in the conversation
            messages = await message_crud.get_by_conversation(
                session, 
                ticket.conversation_id, 
                limit=1000
            )
            
            # Delete each message
            for message in messages:
                await message_crud.remove(session, id=message.id)
            
            # Delete the conversation
            await conversation_crud.remove(session, id=ticket.conversation_id)
        
        # Delete the ticket
        await self.remove(session, id=ticket_id)
        
        return True


# Singleton instance
ticket_crud = CRUDTicket(Ticket)
