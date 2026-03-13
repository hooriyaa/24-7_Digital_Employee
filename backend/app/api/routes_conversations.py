"""
Conversation API routes.

Endpoints for conversation and message retrieval.
"""
import uuid
import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_db_session
from app.crud import message_crud, conversation_crud
from app.models.message import Message
from app.models.conversation import Conversation

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/conversations", tags=["Conversations"])


@router.get(
    "/{conversation_id}/messages",
    summary="Get Conversation Messages",
    description="Retrieve all messages for a conversation",
)
async def get_conversation_messages(
    conversation_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> list[Message]:
    """
    Get all messages for a conversation.

    Args:
        conversation_id: Conversation UUID
        db: Database session

    Returns:
        list[Message]: List of messages ordered by creation time

    Raises:
        HTTPException: If conversation not found
    """
    # Verify conversation exists
    conversation = await conversation_crud.get(db, id=conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found",
        )

    # Get messages
    messages = await message_crud.get_by_conversation(db, conversation_id, limit=100)
    return messages


@router.get(
    "/{conversation_id}",
    summary="Get Conversation",
    description="Retrieve a conversation by ID",
)
async def get_conversation(
    conversation_id: uuid.UUID,
    db: Annotated[AsyncSession, Depends(get_db_session)],
) -> Conversation:
    """
    Get a conversation by ID.

    Args:
        conversation_id: Conversation UUID
        db: Database session

    Returns:
        Conversation: The requested conversation

    Raises:
        HTTPException: If conversation not found
    """
    conversation = await conversation_crud.get(db, id=conversation_id)
    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Conversation {conversation_id} not found",
        )
    return conversation
