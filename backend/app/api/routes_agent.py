"""
Agent API routes.

Endpoints for AI response generation and agent management.
"""
import uuid
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.schemas.agent import AgentRequest, AgentResponse, AgentStatus
from app.agent import create_fte_agent
from app.services.escalation import escalation_service
from app.crud import ticket_crud, message_crud, customer_crud
from app.services.channels import ultramsg_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/agent", tags=["Agent"])


# Zero UUID placeholder check
ZERO_UUID = uuid.UUID("00000000-0000-0000-0000-000000000000")


@router.post(
    "/respond",
    response_model=AgentResponse,
    status_code=status.HTTP_200_OK,
    summary="Generate AI Response",
    description="Generate an AI response for a ticket",
)
async def generate_response(
    request: AgentRequest,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> AgentResponse:
    """
    Generate AI response for a ticket.

    This endpoint:
    1. Validates the ticket_id
    2. Fetches the ticket and conversation
    3. Analyzes sentiment of latest message
    4. Generates response using FTE Agent
    5. Evaluates escalation rules
    6. Returns response with metadata
    """
    # Validate ticket_id is not a placeholder
    if request.ticket_id == ZERO_UUID or str(request.ticket_id) == "00000000-0000-0000-0000-000000000000":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Please select a valid ticket from the Tickets page before sending a message.",
        )

    # Fetch ticket
    ticket = await ticket_crud.get(db, id=request.ticket_id)

    if not ticket:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ticket {request.ticket_id} not found. Please select a valid ticket.",
        )

    # Fetch latest message
    messages = await message_crud.get_by_conversation(
        db,
        conversation_id=ticket.conversation_id,
        limit=1,
    )

    if not messages:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No messages in conversation",
        )

    latest_message = messages[0]

    # Fetch ALL conversation history for context
    all_messages = await message_crud.get_by_conversation(
        db,
        conversation_id=ticket.conversation_id,
        limit=50,
    )

    # Fetch customer details
    customer = await customer_crud.get(db, id=ticket.customer_id)

    # Create FTE agent
    agent = create_fte_agent()

    # Analyze sentiment
    sentiment_result = await agent.analyze_sentiment(latest_message.content)

    # Build comprehensive context for agent
    conversation_history_text = "\n".join([
        f"{'Customer' if msg.sender_type == 'customer' else 'AI Assistant'} ({msg.created_at.strftime('%I:%M %p') if msg.created_at else 'Unknown'}): {msg.content}"
        for msg in all_messages
    ])

    context = {
        "ticket_id": str(ticket.id),
        "customer_id": str(ticket.customer_id),
        "customer_email": customer.email if customer else "unknown",
        "customer_name": customer.name if customer else "unknown",
        "status": ticket.status,
        "priority": ticket.priority,
        "subject": ticket.subject,
        "sentiment_score": sentiment_result.get("score", 0.0),
        "conversation_history": conversation_history_text,
        "message_count": len(all_messages),
        "instructions": """
IMPORTANT: You already have the customer's email and conversation history in the context above.
DO NOT ask for customer ID or email again unless absolutely necessary.
Use the conversation history to understand what has already been discussed.
If the customer is frustrated about repeating information, apologize and continue with the conversation.
""",
    }

    # Generate response with detailed error logging
    try:
        logger.info(f"Generating response for ticket {ticket.id}, subject: {ticket.subject}")
        logger.info(f"Using context: {context}")
        
        response_text = await agent.generate_response(
            input_text=latest_message.content,
            context=context,
        )

        logger.info(f"Response generated successfully for ticket {ticket.id}")

        # Evaluate escalation
        escalation_result = escalation_service.should_escalate(
            confidence_score=0.8,  # Would come from agent
            sentiment_score=sentiment_result.get("score", 0.0),
            message_text=latest_message.content,
        )

        # Send WhatsApp notification for ticket updates
        try:
            # Get customer phone from database
            customer = await customer_crud.get(db, id=ticket.customer_id)
            if customer and customer.phone:
                # Send notification
                await ultramsg_service.send_message(
                    phone=customer.phone,
                    message=f"Ticket Update: {ticket.subject}\nStatus: {ticket.status}\nResponse: {response_text[:100]}...",
                )
        except Exception as e:
            logger.warning(f"WhatsApp notification error: {e}")
            # Continue even if notification fails

        return AgentResponse(
            response=response_text,
            provider="gemini",  # From provider manager
            confidence_score=0.8,
            sentiment_score=sentiment_result.get("score", 0.0),
            requires_escalation=escalation_result.should_escalate,
            escalation_reason=escalation_result.reason.value if escalation_result.reason else None,
            tokens_used=0,  # Would track from provider
        )

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log detailed error information
        error_type = type(e).__name__
        error_message = str(e)
        logger.error(f"Error generating response for ticket {ticket.id}: {error_type} - {error_message}")
        
        # Check for specific error types
        if "authentication" in error_message.lower() or "api key" in error_message.lower():
            logger.error("Authentication error - check API keys in .env file")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI service authentication failed: {error_message}. Check API keys configuration.",
            )
        elif "rate limit" in error_message.lower():
            logger.error("Rate limit exceeded")
            raise HTTPException(
                status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                detail=f"AI service rate limit exceeded: {error_message}",
            )
        elif "connection" in error_message.lower() or "timeout" in error_message.lower():
            logger.error("Connection error")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail=f"AI service connection error: {error_message}",
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error generating response: {error_type} - {error_message}",
            )


@router.get(
    "/providers",
    response_model=AgentStatus,
    summary="Provider Status",
    description="Get all AI provider status and usage",
)
async def get_providers() -> AgentStatus:
    """Get status of all AI providers."""
    from app.agent.providers import provider_manager
    
    providers = provider_manager.get_provider_status()
    active = provider_manager.get_active_provider()
    
    return AgentStatus(
        status="healthy",
        active_provider=active.name if active else "none",
        available_providers=[p["name"] for p in providers],
    )
