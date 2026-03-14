"""
Tickets API routes.

Endpoints for ticket CRUD operations.
"""
import uuid
import logging
from typing import Annotated
from pydantic import BaseModel

from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database import get_db_session
from app.crud import ticket_crud, customer_crud, message_crud, conversation_crud
from app.crud.ticket import TicketCreate
from app.crud.message import MessageCreate
from app.crud.conversation import ConversationCreate
from app.models.ticket import Ticket
from app.models.customer import Customer
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.agent import AgentRequest
from app.services.automation.auto_responder import auto_responder_service
from app.services.gmail import gmail_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tickets", tags=["Tickets"])


async def send_ticket_confirmation_email(
    customer_email: str,
    customer_name: str,
    ticket_id: str,
    subject: str,
    message: str,
    channel: str = "web",  # Add channel parameter
) -> None:
    """
    Send ticket confirmation email to customer.
    
    Args:
        customer_email: Customer email address
        customer_name: Customer name
        ticket_id: Ticket ID
        subject: Ticket subject
        message: Original message
        channel: Channel source (web/email/whatsapp)
    """
    email_subject = f"Ticket Created: {subject} (ID: {ticket_id[:8]}...)"

    # Build email body - include track link only for web form
    email_body = f"""
Dear {customer_name},

Thank you for contacting Customer Support!

Your ticket has been created successfully:

Ticket ID: {ticket_id}
Subject: {subject}

Your Message:
{message}

Our AI assistant is reviewing your request and will respond within 5 minutes.

"""
    
    # Only include track link for web form submissions
    if channel == "web":
        email_body += f"""
You can track your ticket status at: http://localhost:3000/check-status?ticket={ticket_id}

"""
    
    email_body += """
Best regards,
Customer Support Team
"""

    try:
        await gmail_service.send_email(
            to=customer_email,
            subject=email_subject,
            body=email_body,
            html=False,
        )
        logger.info(f"✅ Confirmation email sent to {customer_email}")
    except Exception as e:
        logger.error(f"❌ Failed to send confirmation email: {e}")


class MessageRequest(BaseModel):
    content: str
    sender_type: str = "customer"
    channel: str = "web"
    role: str = "user"


@router.get(
    "",
    summary="Get All Tickets",
    description="Retrieve all tickets from the database",
)
async def get_tickets(
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[dict]:
    """
    Get all tickets from the database with latest message content.

    Returns:
        list[dict]: List of all tickets with latest_message field
    """
    # Get all tickets
    tickets = await ticket_crud.get_multi(db, limit=100)
    
    # Fetch latest message for each ticket
    result = []
    for ticket in tickets:
        ticket_dict = ticket.model_dump()
        
        # Get latest message from conversation
        if ticket.conversation_id:
            latest_message = await message_crud.get_last_message(db, ticket.conversation_id)
            ticket_dict["latest_message"] = latest_message.content if latest_message else None
        else:
            ticket_dict["latest_message"] = None
        
        result.append(ticket_dict)
    
    return result


class TicketStatusResponse(BaseModel):
    """Response model for ticket status lookup."""
    ticket_id: str
    subject: str
    status: str
    priority: str
    created_at: str
    updated_at: str | None = None
    resolved_at: str | None = None
    customer_name: str
    customer_email: str
    messages: list[dict]
    message_count: int


@router.get(
    "/status",
    summary="Check Ticket Status",
    description="Check ticket status by ticket ID or customer email",
    response_model=TicketStatusResponse,
)
async def check_ticket_status(
    db: Annotated[AsyncSession, Depends(get_db_session)],
    ticket_id: str | None = None,
    email: str | None = None,
) -> TicketStatusResponse:
    """
    Check ticket status by ticket ID or customer email.

    This endpoint allows customers to track their support tickets
    without logging in. They can search by:
    - Ticket ID (e.g., TKT-12345)
    - Customer email address

    Args:
        ticket_id: Optional ticket ID (UUID or short form like TKT-12345)
        email: Optional customer email address
        db: Database session

    Returns:
        TicketStatusResponse: Ticket details with messages

    Raises:
        HTTPException: If ticket not found or both parameters missing
    """
    from app.models.customer import Customer
    from app.models.message import Message

    # Validate at least one parameter
    if not ticket_id and not email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please provide either ticket_id or email",
        )

    try:
        # Search by ticket ID
        if ticket_id:
            logger.info(f"🔍 Searching ticket by ID: {ticket_id}")
            
            # Try to parse as UUID first
            try:
                ticket_uuid = uuid.UUID(ticket_id)
                ticket = await ticket_crud.get(db, id=ticket_uuid)
            except ValueError:
                # Not a UUID, search by subject or get all and filter
                tickets = await ticket_crud.get_multi(db, limit=100)
                ticket = None
                for t in tickets:
                    if str(t.id).endswith(ticket_id[-8:]) or t.subject.lower().find(ticket_id.lower()) != -1:
                        ticket = t
                        break

            if not ticket:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Ticket {ticket_id} not found",
                )

        # Search by email
        elif email:
            logger.info(f"🔍 Searching tickets by email: {email}")
            
            # Find customer by email
            customer = await customer_crud.get_by_email(db, email=email)
            if not customer:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No customer found with email: {email}",
                )

            # Get customer's latest ticket
            tickets = await ticket_crud.get_multi(
                db,
                filters={"customer_id": customer.id},
                limit=1,
            )
            if not tickets:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"No tickets found for email: {email}",
                )
            
            ticket = tickets[0]
            logger.info(f"✅ Found ticket {ticket.id} for customer {email}")

        # Get customer details
        customer = await customer_crud.get(db, id=ticket.customer_id)
        if not customer:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Customer not found",
            )

        # Get messages from conversation
        messages = []
        if ticket.conversation_id:
            conversation_messages = await message_crud.get_by_conversation(
                db,
                conversation_id=ticket.conversation_id,
                limit=50,
            )
            messages = [
                {
                    "id": str(msg.id),
                    "content": msg.content,
                    "sender_type": msg.sender_type,
                    "role": msg.role,
                    "channel": msg.channel,
                    "created_at": msg.created_at.isoformat() if msg.created_at else None,
                }
                for msg in conversation_messages
            ]

        # Build response
        return TicketStatusResponse(
            ticket_id=str(ticket.id),
            subject=ticket.subject or "Support Request",
            status=ticket.status,
            priority=ticket.priority or "normal",
            created_at=ticket.created_at.isoformat() if ticket.created_at else None,
            updated_at=getattr(ticket, 'updated_at', None),
            resolved_at=ticket.resolved_at.isoformat() if ticket.resolved_at else None,
            customer_name=customer.name or customer.email,
            customer_email=customer.email,
            messages=messages,
            message_count=len(messages),
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"❌ Error checking ticket status: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to check ticket status: {str(e)}",
        )


@router.get(
    "/{ticket_id}",
    summary="Get Ticket by ID",
    description="Retrieve a specific ticket by ID",
)
async def get_ticket(
    ticket_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Ticket:
    """
    Get a specific ticket by ID.

    Args:
        ticket_id: Ticket UUID
        db: Database session

    Returns:
        Ticket: The requested ticket

    Raises:
        HTTPException: If ticket not found
    """
    ticket = await ticket_crud.get(db, id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )
    return ticket


@router.post(
    "",
    summary="Create New Ticket",
    description="Create a new support ticket with customer and conversation",
    status_code=status.HTTP_201_CREATED,
)
async def create_ticket(
    request: AgentRequest,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Ticket:
    """
    Create a new support ticket.

    This endpoint:
    1. Gets or creates a customer by email
    2. Creates a new conversation
    3. Creates the ticket with the provided data
    4. Creates the initial message in the conversation
    5. Triggers auto-responder in background (Smart Jawab)

    Args:
        request: Ticket creation request with customer data and message
        background_tasks: FastAPI background tasks
        db: Database session

    Returns:
        Ticket: The created ticket

    Raises:
        HTTPException: If customer creation fails or ticket creation fails
    """
    logger.info(f"🎫 CREATE TICKET REQUEST: {request}")
    logger.info(f"📋 Request fields:")
    logger.info(f"   - subject: {request.subject}")
    logger.info(f"   - message: {request.message}")
    logger.info(f"   - customer_email: {request.customer_email}")
    logger.info(f"   - customer_name: {request.customer_name}")

    try:
        # Step 1: Validate required fields
        if not request.customer_email:
            logger.error("❌ customer_email is required but not provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="customer_email is required",
            )

        if not request.subject:
            logger.error("❌ subject is required but not provided")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="subject is required",
            )

        logger.info(f"📧 Customer email: {request.customer_email}")
        logger.info(f"👤 Customer name: {request.customer_name}")
        
        # Step 2: Get or create customer by email
        customer = await customer_crud.get_or_create(
            db,
            email=request.customer_email,
            name=request.customer_name or request.customer_email.split("@")[0],
            phone=request.customer_phone,
        )
        customer_id = customer.id
        logger.info(f"✅ Customer obtained: {customer_id} (email: {request.customer_email})")

        # Step 3: Create conversation
        conversation_data = ConversationCreate(
            customer_id=customer_id,
            status="active",
            channel=request.channel or "web",
        )
        conversation = await conversation_crud.create(db, obj_in=conversation_data)
        logger.info(f"✅ Conversation created: {conversation.id}")

        # Step 4: Create ticket with subject
        logger.info(f"🎫 Creating ticket with customer_id={customer_id}, conversation_id={conversation.id}")
        ticket_data = TicketCreate(
            customer_id=customer_id,
            conversation_id=conversation.id,
            status="open",
            priority=request.priority or "normal",
            subject=request.subject,  # Include subject
        )
        ticket = await ticket_crud.create(db, obj_in=ticket_data)
        logger.info(f"✅ Ticket created: {ticket.id}")

        # Step 5: Create initial message
        if request.message:
            logger.info(f"💬 Creating message with content: {request.message[:50]}...")
            message_data = MessageCreate(
                conversation_id=conversation.id,
                sender_type="customer",
                channel=request.channel or "web",
                content=request.message,
                role="user",
            )
            message = await message_crud.create(db, obj_in=message_data)
            logger.info(f"✅ Message created: {message.id}")
            logger.info(f"📋 Message.content stored as: {message.content[:50]}...")
            
            # Step 6: Trigger auto-responder in background (Smart Jawab)
            logger.info(f"🤖 Triggering auto-responder for ticket {ticket.id}")
            print(f"\n🤖 [ROUTES_TICKETS] Adding background task for auto-responder")
            print(f"🤖 [ROUTES_TICKETS] Ticket ID: {ticket.id}")
            print(f"🤖 [ROUTES_TICKETS] Conversation ID: {conversation.id}")
            print(f"🤖 [ROUTES_TICKETS] Message: {request.message[:50]}...")
            
            # Store conversation_id for background task
            conversation_id = conversation.id
            
            background_tasks.add_task(
                auto_responder_service.process_message,
                db,
                ticket_id=ticket.id,
                message_text=request.message,
                customer_email=request.customer_email,
                customer_phone=customer.phone,
            )
            
            # Send confirmation email
            background_tasks.add_task(
                send_ticket_confirmation_email,
                customer_email=request.customer_email,
                customer_name=request.customer_name or "Valued Customer",
                ticket_id=str(ticket.id),
                subject=ticket.subject,
                message=request.message,
            )
            
            logger.info(f"🤖 Auto-responder background task added")
            logger.info(f"📧 Email confirmation background task added")
        else:
            logger.info("⚠️  No message content provided")

        logger.info(f"🎉 SUCCESS: Ticket {ticket.id} created successfully")
        logger.info(f"📊 Summary:")
        logger.info(f"   - Ticket ID: {ticket.id}")
        logger.info(f"   - Customer ID: {customer_id}")
        logger.info(f"   - Conversation ID: {conversation.id}")
        logger.info(f"   - Subject: {ticket.subject}")
        if request.message:
            logger.info(f"   - Message ID: {message.id}")
            logger.info(f"   - Message Content: {message.content[:50]}...")
        return ticket

    except HTTPException:
        logger.error("❌ HTTPException raised")
        raise
    except Exception as e:
        logger.error(f"❌ ERROR creating ticket: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create ticket: {str(e)}",
        )


@router.put(
    "/{ticket_id}",
    summary="Update Ticket",
    description="Update an existing ticket",
)
async def update_ticket(
    ticket_id: uuid.UUID,
    updates: dict,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Ticket:
    """
    Update a ticket.

    Args:
        ticket_id: Ticket UUID
        updates: Fields to update
        db: Database session

    Returns:
        Ticket: Updated ticket

    Raises:
        HTTPException: If ticket not found
    """
    ticket = await ticket_crud.update_by_id(db, id=ticket_id, obj_in=updates)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )
    return ticket


@router.post(
    "/{ticket_id}/escalate",
    summary="Escalate Ticket",
    description="Mark a ticket as escalated",
)
async def escalate_ticket(
    ticket_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Ticket:
    """
    Escalate a ticket to human agent.

    Args:
        ticket_id: Ticket UUID
        db: Database session

    Returns:
        Ticket: Updated ticket with status='escalated'

    Raises:
        HTTPException: If ticket not found
    """
    ticket = await ticket_crud.update_by_id(
        db,
        id=ticket_id,
        obj_in={"status": "escalated"},
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )
    logger.info(f"Escalated ticket: {ticket_id}")
    return ticket


@router.post(
    "/{ticket_id}/resolve",
    summary="Resolve Ticket",
    description="Mark a ticket as resolved",
)
async def resolve_ticket(
    ticket_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Ticket:
    """
    Resolve a ticket.

    Args:
        ticket_id: Ticket UUID
        db: Database session

    Returns:
        Ticket: Updated ticket with status='resolved'

    Raises:
        HTTPException: If ticket not found
    """
    from datetime import datetime, timezone

    ticket = await ticket_crud.update_by_id(
        db,
        id=ticket_id,
        obj_in={
            "status": "resolved",
            "resolved_at": datetime.now(timezone.utc),
        },
    )
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )
    logger.info(f"Resolved ticket: {ticket_id}")
    return ticket


@router.post(
    "/{ticket_id}/messages",
    summary="Send Message to Ticket",
    description="Send a message to a ticket and trigger AI response",
    status_code=status.HTTP_201_CREATED,
)
async def send_ticket_message(
    ticket_id: uuid.UUID,
    request: MessageRequest,
    background_tasks: BackgroundTasks,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Message:
    """
    Send a message to a ticket.

    This endpoint:
    1. Gets the ticket and conversation
    2. Creates the message in the conversation
    3. Triggers auto-responder in background

    Args:
        ticket_id: Ticket UUID
        request: Message request with content and metadata
        background_tasks: FastAPI background tasks
        db: Database session

    Returns:
        Message: The created message

    Raises:
        HTTPException: If ticket not found or message creation fails
    """
    logger.info(f"📩 Sending message to ticket {ticket_id}")
    
    # Get ticket
    ticket = await ticket_crud.get(db, id=ticket_id)
    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )
    
    if not ticket.conversation_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Ticket {ticket_id} has no conversation",
        )
    
    # Create message
    message_data = MessageCreate(
        conversation_id=ticket.conversation_id,
        sender_type=request.sender_type,
        channel=request.channel,
        content=request.content,
        role=request.role,
    )
    
    message = await message_crud.create(db, obj_in=message_data)
    logger.info(f"✅ Message created: {message.id}")
    
    # Trigger auto-responder in background
    if request.sender_type == "customer":
        logger.info(f"🤖 Triggering auto-responder for message {message.id}")
        background_tasks.add_task(
            auto_responder_service.process_message,
            db,
            ticket_id=ticket_id,
            message_text=request.content,
            customer_email="",  # Will be fetched in the service
            customer_phone=None,
        )
    
    return message


@router.delete(
    "/{ticket_id}",
    summary="Delete Ticket",
    description="Delete a ticket and all its messages",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def delete_ticket(
    ticket_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> None:
    """
    Delete a ticket and all associated messages.

    This endpoint:
    1. Deletes all messages in the ticket's conversation
    2. Deletes the conversation
    3. Deletes the ticket

    Args:
        ticket_id: Ticket UUID
        db: Database session

    Raises:
        HTTPException: If ticket not found
    """
    success = await ticket_crud.delete_ticket_with_messages(db, ticket_id=ticket_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {ticket_id} not found",
        )

    logger.info(f"Deleted ticket and associated messages: {ticket_id}")
