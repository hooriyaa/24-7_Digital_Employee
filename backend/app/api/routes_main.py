"""
Main API routes for Tickets, Customers, and Knowledge Base.

These endpoints provide CRUD operations for the frontend.
"""
import uuid
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.database import get_db_session
from app.models.ticket import Ticket
from app.models.customer import Customer
from app.models.knowledge_base import KnowledgeBase

router = APIRouter()


# ==================== TICKETS ====================

@router.get("/tickets", response_model=list[Ticket])
async def get_tickets(
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Get all tickets from the database.
    
    Returns a list of all tickets with their associated customer information.
    """
    result = await db.exec(select(Ticket).order_by(Ticket.created_at.desc()))
    tickets = result.all()
    return tickets


@router.get("/tickets/{ticket_id}", response_model=Ticket)
async def get_ticket(
    ticket_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Get a specific ticket by ID.
    """
    ticket = await db.get(Ticket, ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    return ticket


# Note: POST /tickets is now handled by routes_tickets.py with proper customer/conversation creation


@router.put("/tickets/{ticket_id}", response_model=Ticket)
async def update_ticket(
    ticket_id: uuid.UUID,
    ticket_update: Ticket,
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Update an existing ticket.
    """
    db_ticket = await db.get(Ticket, ticket_id)
    if not db_ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Ticket not found",
        )
    
    # Update fields
    update_data = ticket_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_ticket, key, value)
    
    db.add(db_ticket)
    await db.commit()
    await db.refresh(db_ticket)
    return db_ticket


# ==================== CUSTOMERS ====================

@router.get("/customers", response_model=list[Customer])
async def get_customers(
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Get all customers from the database.
    """
    result = await db.exec(select(Customer).order_by(Customer.created_at.desc()))
    customers = result.all()
    return customers


@router.get("/customers/{customer_id}", response_model=Customer)
async def get_customer(
    customer_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Get a specific customer by ID.
    """
    customer = await db.get(Customer, customer_id)
    if not customer:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found",
        )
    return customer


@router.get("/customers/lookup", response_model=Customer | None)
async def lookup_customer(
    email: str,
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Lookup customer by email.
    """
    result = await db.exec(select(Customer).where(Customer.email == email))
    return result.first()


# ==================== KNOWLEDGE BASE ====================

@router.get("/knowledge-base", response_model=list[KnowledgeBase])
async def get_knowledge_base(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    category: str | None = None,
    active_only: bool = True,
):
    """
    Get all knowledge base articles.
    
    Args:
        category: Optional category filter
        active_only: Only return active articles (default: True)
    """
    statement = select(KnowledgeBase)
    
    if category:
        statement = statement.where(KnowledgeBase.category == category)
    
    if active_only:
        statement = statement.where(KnowledgeBase.is_active == True)
    
    statement = statement.order_by(KnowledgeBase.created_at.desc())
    
    result = await db.exec(statement)
    return result.all()


@router.get("/knowledge-base/{article_id}", response_model=KnowledgeBase)
async def get_knowledge_article(
    article_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
):
    """
    Get a specific knowledge base article by ID.
    """
    article = await db.get(KnowledgeBase, article_id)
    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )
    return article
