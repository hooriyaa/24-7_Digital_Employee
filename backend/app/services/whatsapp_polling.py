"""
WhatsApp Polling Service - UltraMsg Integration.

Polls UltraMsg API every 30 seconds to check for new messages.
No webhook required! No ngrok required!
"""
import asyncio
import logging
import os
import httpx
from datetime import datetime, timezone
from typing import Optional

from app.database import get_db_session
from app.crud import customer_crud, ticket_crud, message_crud, conversation_crud
from app.crud.ticket import TicketCreate
from app.crud.message import MessageCreate
from app.crud.conversation import ConversationCreate
from app.services.automation.auto_responder import auto_responder_service
from app.services.ultramsg import ultramsg_service

logger = logging.getLogger(__name__)


class WhatsAppPollingService:
    """
    WhatsApp Polling Service.
    
    Polls UltraMsg API every 30 seconds to check for new messages.
    """
    
    def __init__(self):
        """Initialize WhatsApp polling service."""
        self.instance_id = os.getenv("ULTRAMSG_INSTANCE_ID", "")
        self.token = os.getenv("ULTRAMSG_TOKEN", "")
        self.base_url = "https://api.ultramsg.com"
        self.enabled = bool(self.instance_id and self.token)
        self.polling_interval = 30  # seconds
        self._running = False
        self._last_message_time = 0
        self._processed_messages = set()
    
    async def get_received_messages(self, limit: int = 10) -> list:
        """
        Get received messages from UltraMsg API.
        
        Args:
            limit: Maximum number of messages to fetch
            
        Returns:
            List of received messages
        """
        if not self.enabled:
            logger.warning("WhatsApp polling not enabled (missing credentials)")
            logger.warning(f"Instance ID: {self.instance_id}")
            logger.warning(f"Token: {self.token[:10]}...")
            return []
        
        try:
            url = f"{self.base_url}/{self.instance_id}/messages/received"
            params = {
                "token": self.token,
                "limit": limit,
            }
            
            logger.info(f"📡 Fetching messages from: {url}")
            logger.info(f"📡 Params: token={self.token[:10]}..., limit={limit}")
            logger.info(f"📡 Full URL: {url}?token={self.token[:10]}...&limit={limit}")
            
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url, params=params)
                
                logger.info(f"📡 Response status: {response.status_code}")
                logger.info(f"📡 Response headers: {dict(response.headers)}")
                logger.info(f"📡 Response body: {response.text[:500]}")
                
                if response.status_code == 200:
                    data = response.json()
                    logger.info(f"📡 Parsed JSON: {data}")
                    messages = data.get("messages", [])
                    logger.info(f"✅ Fetched {len(messages)} messages from UltraMsg")
                    
                    # Log message details
                    for i, msg in enumerate(messages):
                        logger.info(f"📨 Message {i+1}: from={msg.get('from')}, body={msg.get('body', '')[:50]}")
                    
                    return messages
                else:
                    logger.error(f"❌ UltraMsg API error: {response.status_code}")
                    logger.error(f"❌ Response: {response.text}")
                    return []
                    
        except httpx.ConnectError as e:
            logger.error(f"❌ Network error (check internet): {e}")
            logger.error(f"❌ Trying to connect to: {self.base_url}")
            return []
        except httpx.TimeoutException as e:
            logger.error(f"❌ Timeout error (API slow): {e}")
            return []
        except Exception as e:
            logger.error(f"❌ Failed to fetch messages: {e}", exc_info=True)
            return []
    
    async def process_message(self, message_data: dict, db) -> None:
        """
        Process a single received message.
        
        Args:
            message_data: Message data from UltraMsg API
            db: Database session
        """
        try:
            # Extract message data
            message_id = message_data.get("id", "")
            from_phone = message_data.get("from", "")
            message_text = message_data.get("body", "") or message_data.get("text", "")
            message_time = message_data.get("time", 0)
            
            # Skip if already processed
            if message_id in self._processed_messages:
                logger.debug(f"⏭️  Skipping already processed message: {message_id}")
                return
            
            # Skip old messages
            if message_time < self._last_message_time:
                logger.debug(f"⏭️  Skipping old message: {message_id}")
                return
            
            logger.info(f"📱 New WhatsApp message from: {from_phone}")
            logger.info(f"💬 Message: {message_text[:50]}...")
            
            # Mark as processed
            self._processed_messages.add(message_id)
            self._last_message_time = message_time
            
            # Step 1: Get or create customer by phone
            customer = await customer_crud.get_or_create_by_phone(
                db,
                phone=from_phone,
                name=f"WhatsApp User {from_phone[-4:]}",
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
            message_data_obj = MessageCreate(
                conversation_id=ticket.conversation_id,
                sender_type="customer",
                channel="whatsapp",
                content=message_text,
                role="user",
            )
            message = await message_crud.create(db, obj_in=message_data_obj)
            logger.info(f"✅ Message saved: {message.id}")
            
            # Step 4: Trigger auto-responder
            logger.info(f"🤖 Triggering auto-responder for WhatsApp message")
            
            await auto_responder_service.process_message(
                db,
                ticket_id=ticket.id,
                message_text=message_text,
                customer_email=customer.email,
                customer_phone=from_phone,
            )
            
            logger.info(f"✅ WhatsApp message processed successfully!")
            
        except Exception as e:
            logger.error(f"❌ Failed to process message: {e}", exc_info=True)
    
    async def poll_messages(self) -> None:
        """
        Poll for new messages and process them.
        """
        logger.info("🔄 Starting poll_messages...")
        try:
            # Get database session
            async for db in get_db_session():
                logger.info("📡 DB session obtained, fetching messages...")
                # Fetch messages
                messages = await self.get_received_messages(limit=10)
                logger.info(f"📦 Got {len(messages)} messages to process")

                # Process each message
                for message_data in messages:
                    logger.info(f"📨 Processing message: {message_data.get('id', 'unknown')}")
                    await self.process_message(message_data, db)

                # Close DB session
                await db.close()
                logger.info("✅ poll_messages completed")
                break

        except Exception as e:
            logger.error(f"❌ Polling error: {e}", exc_info=True)
    
    async def start_polling(self) -> None:
        """
        Start polling loop.
        """
        logger.info("📱 Starting WhatsApp polling service...")
        logger.info(f"⏰ Polling interval: {self.polling_interval} seconds")
        self._running = True
        
        poll_count = 0

        while self._running:
            poll_count += 1
            logger.info(f"🔄 Polling iteration #{poll_count}")
            try:
                await self.poll_messages()
            except Exception as e:
                logger.error(f"❌ Polling loop error: {e}", exc_info=True)

            # Wait for next poll
            logger.info(f"⏳ Waiting {self.polling_interval} seconds for next poll...")
            await asyncio.sleep(self.polling_interval)
    
    def stop_polling(self) -> None:
        """
        Stop polling loop.
        """
        logger.info("📱 Stopping WhatsApp polling service...")
        self._running = False


# Singleton instance
whatsapp_polling_service = WhatsAppPollingService()
