"""
Gmail Webhook Handler - Gmail API Integration.

Receives incoming emails and sends responses.
"""
import logging
import base64
from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel, EmailStr

from app.database import get_db_session
from app.crud import customer_crud, ticket_crud, message_crud, conversation_crud
from app.crud.ticket import TicketCreate
from app.crud.message import MessageCreate
from app.crud.conversation import ConversationCreate
from app.services.automation.auto_responder import auto_responder_service
from app.services.gmail import gmail_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/gmail", tags=["Gmail Webhook"])


class GmailWebhook(BaseModel):
    """Gmail incoming message webhook payload."""
    from_email: EmailStr
    to_email: EmailStr
    subject: str
    body: str
    message_id: Optional[str] = None
    thread_id: Optional[str] = None


@router.post("/webhook")
async def gmail_incoming_webhook(
    webhook_data: GmailWebhook,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> dict:
    """
    Receive incoming emails via Gmail webhook.
    
    This endpoint:
    1. Gets or creates customer by email
    2. Creates or gets active ticket
    3. Saves message to conversation
    4. Triggers AI auto-responder
    5. Sends response via Gmail
    
    Args:
        webhook_data: Gmail message data
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        dict: Success response
    """
    logger.info(f"📧 Gmail webhook received from: {webhook_data.from_email}")
    logger.info(f"📝 Subject: {webhook_data.subject}")
    logger.info(f"💬 Message: {webhook_data.body[:50]}...")
    
    try:
        # Step 1: Get or create customer by email
        customer = await customer_crud.get_or_create(
            db,
            email=webhook_data.from_email,
            name=webhook_data.from_email.split("@")[0],
        )
        customer_id = customer.id
        logger.info(f"✅ Customer obtained: {customer_id}")
        
        # Step 2: Get or create active ticket for this customer
        existing_tickets = await ticket_crud.get_multi(
            db,
            filters={"customer_id": customer_id},
            limit=1,
        )
        
        if existing_tickets:
            ticket = existing_tickets[0]
            logger.info(f"📋 Using existing ticket: {ticket.id}")
        else:
            # Create new conversation
            conversation_data = ConversationCreate(
                customer_id=customer_id,
                status="active",
                channel="email",
            )
            conversation = await conversation_crud.create(db, obj_in=conversation_data)
            
            # Create new ticket
            ticket_data = TicketCreate(
                customer_id=customer_id,
                conversation_id=conversation.id,
                status="open",
                priority="normal",
                subject=webhook_data.subject or "Email Support Request",
            )
            ticket = await ticket_crud.create(db, obj_in=ticket_data)
            logger.info(f"🎫 New ticket created: {ticket.id}")
        
        # Step 3: Save incoming message
        message_data = MessageCreate(
            conversation_id=ticket.conversation_id,
            sender_type="customer",
            channel="email",
            content=webhook_data.body,
            role="user",
        )
        message = await message_crud.create(db, obj_in=message_data)
        logger.info(f"✅ Message saved: {message.id}")
        
        # Step 4: Trigger auto-responder in background
        background_tasks.add_task(
            auto_responder_service.process_message,
            db,
            ticket_id=ticket.id,
            message_text=webhook_data.body,
            customer_email=webhook_data.from_email,
            customer_phone=customer.phone,
        )
        logger.info(f"🤖 Auto-responder triggered for Gmail message")
        
        return {
            "status": "success",
            "ticket_id": str(ticket.id),
            "message": "Email received and processing",
        }
        
    except Exception as e:
        logger.error(f"❌ Gmail webhook error: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Processing failed",
        )


@router.get("/test")
async def test_gmail_webhook():
    """Test endpoint to verify Gmail webhook is working."""
    return {
        "status": "ok",
        "message": "Gmail webhook is running",
        "service": "Gmail API",
    }
