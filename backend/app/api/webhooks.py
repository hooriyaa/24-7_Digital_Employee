"""
Webhook handlers for incoming messages from external channels.

Handles:
- WhatsApp (UltraMsg) incoming messages
- Gmail Pub/Sub notifications
"""
import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.crud import customer_crud, ticket_crud, message_crud
from app.services.channels import ultramsg_service, gmail_service
from app.services.channels.whatsapp import UltraMsgService

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])


@router.post("/ultramsg")
async def handle_whatsapp_webhook(
    data: dict,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    background_tasks: BackgroundTasks,
) -> dict:
    """
    Handle incoming WhatsApp messages from UltraMsg.
    
    Webhook payload format:
    {
        "from": "+1234567890",
        "message": "Hello",
        "timestamp": 1234567890,
        "type": "text"
    }
    """
    # Verify webhook
    if not ultramsg_service.verify_webhook(data):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid webhook",
        )
    
    # Parse message
    phone = data.get("from")
    message_text = data.get("message")
    timestamp = data.get("timestamp")
    
    if not phone or not message_text:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Missing from or message field",
        )
    
    # Process in background to avoid timeout
    background_tasks.add_task(
        process_whatsapp_message,
        db,
        phone,
        message_text,
        timestamp,
    )
    
    return {"status": "received"}


async def process_whatsapp_message(
    db: AsyncSession,
    phone: str,
    message_text: str,
    timestamp: int | None = None,
):
    """
    Process incoming WhatsApp message and create/update ticket.
    
    This runs in the background to avoid webhook timeout.
    """
    try:
        from app.models.message import Message
        
        # Find or create customer by phone
        customer = await customer_crud.get_by_phone(db, phone=phone)
        
        if not customer:
            # Create new customer
            from app.models.customer import Customer
            customer = Customer(
                phone=phone,
                name=f"WhatsApp User {phone[-4:]}",
                email=f"whatsapp_{phone[-4:]}@unknown.com",
            )
            db.add(customer)
            await db.flush()
        
        # Find existing open ticket or create new one
        from sqlmodel import select
        from app.models.ticket import Ticket
        
        result = await db.exec(
            select(Ticket)
            .where(Ticket.customer_id == customer.id)
            .where(Ticket.status.in_(["open", "in_progress", "waiting_customer"]))
            .order_by(Ticket.created_at.desc())
            .limit(1)
        )
        existing_ticket = result.first()
        
        if existing_ticket:
            ticket = existing_ticket
            # Add message to existing conversation
            if ticket.conversation_id:
                message = Message(
                    conversation_id=ticket.conversation_id,
                    sender_type="customer",
                    channel="whatsapp",
                    role="user",
                    content=message_text,
                )
                db.add(message)
        else:
            # Create new conversation and ticket
            from app.models.conversation import Conversation
            
            conversation = Conversation(
                customer_id=customer.id,
                status="active",
                message_count=1,
            )
            db.add(conversation)
            await db.flush()
            
            ticket = Ticket(
                customer_id=customer.id,
                conversation_id=conversation.id,
                status="open",
                priority="normal",
                subject=f"WhatsApp message from {phone}",
                channel="whatsapp",
            )
            db.add(ticket)
            await db.flush()
            
            # Create first message
            message = Message(
                conversation_id=conversation.id,
                sender_type="customer",
                channel="whatsapp",
                role="user",
                content=message_text,
            )
            db.add(message)
        
        await db.commit()
        
        print(f"Processed WhatsApp message from {phone} for ticket {ticket.id}")
        
    except Exception as e:
        print(f"Error processing WhatsApp message: {e}")
        await db.rollback()


@router.post("/gmail")
async def handle_gmail_webhook(
    data: dict,
    db: Annotated[AsyncSession, Depends(get_db_session)],
    background_tasks: BackgroundTasks,
) -> dict:
    """
    Handle Gmail Pub/Sub notifications.
    
    This endpoint receives notifications from Gmail when new emails arrive.
    The actual email fetching happens in the background.
    """
    # Verify Gmail headers (in production)
    # X-Google-Channel-ID
    # X-Google-Resource-ID
    # X-Google-Resource-STATE
    
    # Process in background
    background_tasks.add_task(
        process_gmail_notification,
        db,
        data,
    )
    
    return {"status": "received"}


async def process_gmail_notification(
    db: AsyncSession,
    data: dict,
):
    """
    Process Gmail notification and fetch new emails.
    
    This runs in the background to avoid webhook timeout.
    """
    try:
        # Fetch unread emails
        emails = await gmail_service.fetch_emails(
            query="is:unread",
            max_results=10,
        )
        
        for email in emails:
            # Parse email for ticket creation
            parsed = gmail_service.parse_incoming_email(email)
            
            # Find customer by email
            customer = await customer_crud.get_by_email(
                db,
                email=parsed["from"],
            )
            
            if not customer:
                # Create new customer
                from app.models.customer import Customer
                customer = Customer(
                    email=parsed["from"],
                    name=parsed["from"].split("@")[0],
                )
                db.add(customer)
                await db.flush()
            
            # Create ticket for new email
            # (Similar logic to WhatsApp processing)
            
        await db.commit()
        
    except Exception as e:
        print(f"Error processing Gmail notification: {e}")
        await db.rollback()
