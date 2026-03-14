"""
WhatsApp Webhook Handler - UltraMsg Integration.

Receives incoming WhatsApp messages and sends responses.
"""
import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel

from app.database import get_db_session
from app.crud import customer_crud, ticket_crud, message_crud, conversation_crud
from app.crud.ticket import TicketCreate
from app.crud.message import MessageCreate
from app.crud.conversation import ConversationCreate
from app.services.automation.auto_responder import auto_responder_service
from app.services.ultramsg import ultramsg_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/whatsapp", tags=["WhatsApp Webhook"])


class WhatsAppWebhook(BaseModel):
    """WhatsApp incoming message webhook payload."""
    phone: str
    body: str
    type: str = "text"
    time: int | None = None


@router.post("/webhook")
async def whatsapp_incoming_webhook(
    webhook_data: WhatsAppWebhook,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> dict:
    """
    Receive incoming WhatsApp messages via UltraMsg webhook.
    
    This endpoint:
    1. Gets or creates customer by phone
    2. Creates or gets active ticket
    3. Saves message to conversation
    4. Triggers AI auto-responder
    5. Sends response via WhatsApp
    
    Args:
        webhook_data: WhatsApp message data
        background_tasks: FastAPI background tasks
        db: Database session
        
    Returns:
        dict: Success response
    """
    logger.info(f"📱 WhatsApp webhook received from: {webhook_data.phone}")
    logger.info(f"💬 Message: {webhook_data.body[:50]}...")
    
    try:
        # Step 1: Get or create customer by phone
        customer = await customer_crud.get_or_create_by_phone(
            db,
            phone=webhook_data.phone,
            name=f"WhatsApp User {webhook_data.phone[-4:]}",
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
                channel="whatsapp",
            )
            conversation = await conversation_crud.create(db, obj_in=conversation_data)
            
            # Create new ticket
            ticket_data = TicketCreate(
                customer_id=customer_id,
                conversation_id=conversation.id,
                status="open",
                priority="normal",
                subject="WhatsApp Support Request",
            )
            ticket = await ticket_crud.create(db, obj_in=ticket_data)
            logger.info(f"🎫 New ticket created: {ticket.id}")
        
        # Step 3: Save incoming message
        message_data = MessageCreate(
            conversation_id=ticket.conversation_id,
            sender_type="customer",
            channel="whatsapp",
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
            customer_email=customer.email,
            customer_phone=webhook_data.phone,
        )
        logger.info(f"🤖 Auto-responder triggered for WhatsApp message")
        
        return {
            "status": "success",
            "ticket_id": str(ticket.id),
            "message": "Message received and processing",
        }
        
    except Exception as e:
        logger.error(f"❌ WhatsApp webhook error: {e}", exc_info=True)
        # Don't return error to UltraMsg - it will retry
        return {"status": "error", "message": "Processing failed"}


@router.get("/test")
async def test_whatsapp_webhook():
    """Test endpoint to verify WhatsApp webhook is working."""
    return {
        "status": "ok",
        "message": "WhatsApp webhook is running",
        "service": "UltraMsg",
    }
