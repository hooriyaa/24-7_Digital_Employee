"""
CRUD operations for database models.

Provides generic and entity-specific CRUD operations with async support.
"""
from app.crud.base import CRUDBase
from app.crud.customer import customer_crud, CRUDCustomer, CustomerCreate, CustomerUpdate
from app.crud.ticket import ticket_crud, CRUDTicket, TicketCreate, TicketUpdate
from app.crud.message import message_crud, CRUDMessage, MessageCreate, MessageUpdate
from app.crud.conversation import conversation_crud, CRUDConversation, ConversationCreate, ConversationUpdate
from app.crud.knowledge_base import knowledge_base_crud, CRUDKnowledgeBase, KnowledgeBaseCreate, KnowledgeBaseUpdate

__all__ = [
    # Base
    "CRUDBase",
    # Customer
    "customer_crud",
    "CRUDCustomer",
    "CustomerCreate",
    "CustomerUpdate",
    # Ticket
    "ticket_crud",
    "CRUDTicket",
    "TicketCreate",
    "TicketUpdate",
    # Message
    "message_crud",
    "CRUDMessage",
    "MessageCreate",
    "MessageUpdate",
    # Conversation
    "conversation_crud",
    "CRUDConversation",
    "ConversationCreate",
    "ConversationUpdate",
    # Knowledge Base
    "knowledge_base_crud",
    "CRUDKnowledgeBase",
    "KnowledgeBaseCreate",
    "KnowledgeBaseUpdate",
]
