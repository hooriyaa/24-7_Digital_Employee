"""
WhatsApp Webhook Handler - UltraMsg Integration.

Receives incoming WhatsApp messages and sends responses.
"""
import logging
from typing import Annotated, Any
from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, Form, Request
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

router = APIRouter(tags=["WhatsApp Webhook"])


class WhatsAppWebhook(BaseModel):
    """WhatsApp incoming message webhook payload."""
    phone: str
    body: str
    type: str = "text"
    time: int | None = None


@router.post("/webhook")
async def whatsapp_incoming_webhook(
    request: Request,
    background_tasks: BackgroundTasks = None,
    db: Annotated[AsyncSession, Depends(get_db_session)] = None,
) -> dict:
    """
    Receive incoming WhatsApp messages via UltraMsg webhook.
    """
    # Try to get data from both JSON and form-data
    form_data = {}
    json_data = {}
    
    # Try form-data first
    try:
        form_data = await request.form()
        logger.info(f"📋 FORM DATA: {dict(form_data)}")
    except Exception as e:
        logger.debug(f"Not form-data: {e}")
    
    # Try JSON
    try:
        json_data = await request.json()
        logger.info(f"📋 JSON DATA: {json_data}")
    except Exception as e:
        logger.debug(f"Not JSON: {e}")
    
    # Combine both
    all_data = {**dict(form_data), **json_data}
    logger.info(f"📋 COMBINED DATA: {all_data}")
    
    # UltraMsg specific: data is nested inside 'data' field
    nested_data = all_data.get("data", {})
    logger.info(f"📋 NESTED DATA: {nested_data}")
    
    # Handle different field names from UltraMsg
    customer_phone = (
        all_data.get("phone") or 
        all_data.get("from") or 
        nested_data.get("from") or 
        nested_data.get("phone") or 
        all_data.get("sender") or 
        all_data.get("to") or 
        all_data.get("phone_number") or
        ""
    )
    message_body = (
        all_data.get("body") or 
        all_data.get("text") or 
        all_data.get("message") or 
        nested_data.get("body") or 
        nested_data.get("text") or 
        nested_data.get("message") or 
        all_data.get("content") or 
        all_data.get("message_body") or
        ""
    )
    message_type = all_data.get("type", "text") or nested_data.get("type", "text")
    
    logger.info(f"📱 WhatsApp webhook received from: {customer_phone}")
    logger.info(f"💬 Message: {message_body[:50] if message_body else 'EMPTY'}...")
    logger.info(f"📋 Parsed data - phone: '{customer_phone}', body: '{message_body}', type: '{message_type}'")
    
    if not customer_phone or not message_body:
        logger.warning(f"⚠️  Missing phone or body in webhook data")
        logger.warning(f"📋 Available fields: {list(all_data.keys())}")
        logger.warning(f"📋 Nested fields: {list(nested_data.keys()) if nested_data else 'None'}")
        return {"status": "error", "message": "Missing phone or body", "received_fields": list(all_data.keys())}
    
    # Create webhook data object
    webhook_data = WhatsAppWebhook(phone=customer_phone, body=message_body, type=message_type)

    try:
        # Step 1: Get or create customer by phone
        # Try to get customer by phone first
        customer = await customer_crud.get_by_phone(db, phone=customer_phone)
        
        if not customer:
            # Create new customer with phone
            from app.crud.customer import CustomerCreate
            customer_data = CustomerCreate(
                email=f"whatsapp_{customer_phone}@temp.local",
                name=f"WhatsApp User {customer_phone[-4:]}",
                phone=customer_phone,
            )
            customer = await customer_crud.create(db, obj_in=customer_data)
        
        customer_id = customer.id
        logger.info(f"✅ Customer obtained: {customer_id} (phone: {customer_phone})")
        
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
