"""
Gmail Polling Service - Check Gmail for new emails automatically.

Polls Gmail inbox every 30 seconds and processes new emails.
"""
import asyncio
import logging
import email
import imaplib
from datetime import datetime, timedelta, timezone
from typing import Optional
import os

from app.services.gmail import gmail_service
from app.crud import customer_crud, ticket_crud, message_crud, conversation_crud
from app.crud.ticket import TicketCreate
from app.crud.message import MessageCreate
from app.crud.conversation import ConversationCreate
from app.services.automation.auto_responder import auto_responder_service
from app.database import get_db_session

logger = logging.getLogger(__name__)


class GmailPollingService:
    """
    Gmail polling service that checks for new emails periodically.
    """
    
    def __init__(self):
        """Initialize Gmail polling service."""
        self.email = os.getenv("GMAIL_SENDER_EMAIL", "")
        self.password = os.getenv("GMAIL_SENDER_PASSWORD", "")
        self.poll_interval = 30  # Check every 30 seconds
        self.is_running = False
        self.last_check = datetime.now(timezone.utc)
        
    async def start_polling(self):
        """
        Start polling Gmail inbox for new emails.
        Runs in background indefinitely.
        """
        if not self.email or not self.password:
            logger.warning("⚠️  Gmail credentials not configured, polling disabled")
            return
            
        self.is_running = True
        logger.info(f"📧 Starting Gmail polling (every {self.poll_interval}s)")
        
        while self.is_running:
            try:
                await self.check_new_emails()
                await asyncio.sleep(self.poll_interval)
            except Exception as e:
                logger.error(f"❌ Gmail polling error: {e}", exc_info=True)
                await asyncio.sleep(self.poll_interval)
    
    def stop_polling(self):
        """Stop Gmail polling."""
        self.is_running = False
        logger.info("📧 Gmail polling stopped")
    
    async def check_new_emails(self):
        """
        Check Gmail inbox for new unread emails.
        Process each new email and send reply.
        """
        try:
            # Connect to Gmail IMAP
            mail = imaplib.IMAP4_SSL("imap.gmail.com")
            mail.login(self.email, self.password)
            mail.select("inbox")
            
            # Search for unread emails from last poll time
            since_date = self.last_check.strftime("%d-%b-%Y")
            result, data = mail.search(None, f'(UNSEEN SINCE {since_date})')
            
            if result != "OK":
                mail.close()
                mail.logout()
                return
            
            email_ids = data[0].split()
            
            if not email_ids:
                logger.debug("📧 No new emails")
                mail.close()
                mail.logout()
                return
            
            logger.info(f"📧 Found {len(email_ids)} new email(s)")
            
            # Process each new email
            for email_id in email_ids:
                await self.process_email(mail, email_id)
            
            # Update last check time
            self.last_check = datetime.now(timezone.utc)
            
            mail.close()
            mail.logout()
            
        except Exception as e:
            logger.error(f"❌ Error checking emails: {e}", exc_info=True)
    
    async def process_email(self, mail: imaplib.IMAP4_SSL, email_id: bytes):
        """
        Process a single email.
        
        Args:
            mail: IMAP connection
            email_id: Email ID
        """
        try:
            # Fetch email
            result, msg_data = mail.fetch(email_id, "(RFC822)")
            
            if result != "OK":
                return
            
            # Parse email
            raw_email = msg_data[0][1]
            email_message = email.message_from_bytes(raw_email)
            
            # Extract email details
            from_email = email_message.get("From", "")
            to_email = email_message.get("To", "")
            subject = email_message.get("Subject", "")
            
            # Extract body
            body = self._extract_body(email_message)
            
            logger.info(f"📧 Processing email from {from_email}: {subject[:50]}...")
            
            # Process email and send reply
            await self.handle_email(
                from_email=from_email,
                to_email=to_email,
                subject=subject,
                body=body,
            )
            
        except Exception as e:
            logger.error(f"❌ Error processing email: {e}", exc_info=True)
    
    def _extract_body(self, email_message: email.message.Message) -> str:
        """
        Extract body from email message.
        
        Args:
            email_message: Parsed email message
            
        Returns:
            Email body text
        """
        body = ""
        
        if email_message.is_multipart():
            for part in email_message.walk():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition", ""))
                
                # Skip attachments
                if "attachment" in content_disposition:
                    continue
                
                if content_type == "text/plain":
                    try:
                        charset = part.get_content_charset() or "utf-8"
                        body = part.get_payload(decode=True).decode(charset, errors="ignore")
                        break
                    except:
                        pass
        else:
            try:
                charset = email_message.get_content_charset() or "utf-8"
                body = email_message.get_payload(decode=True).decode(charset, errors="ignore")
            except:
                pass
        
        return body.strip()
    
    async def handle_email(
        self,
        from_email: str,
        to_email: str,
        subject: str,
        body: str,
    ):
        """
        Handle incoming email - create ticket and send reply.
        
        Args:
            from_email: Sender email
            to_email: Recipient email
            subject: Email subject
            body: Email body
        """
        try:
            # Get database session
            async for session in get_db_session():
                # Step 1: Get or create customer
                customer = await customer_crud.get_or_create(
                    session,
                    email=from_email.split("<")[-1].strip(">"),
                    name=from_email.split("<")[0].strip() if "<" in from_email else from_email.split("@")[0],
                )
                
                # Step 2: Create conversation
                conversation_data = ConversationCreate(
                    customer_id=customer.id,
                    status="active",
                    channel="email",
                )
                conversation = await conversation_crud.create(session, obj_in=conversation_data)
                
                # Step 3: Create ticket
                ticket_data = TicketCreate(
                    customer_id=customer.id,
                    conversation_id=conversation.id,
                    status="open",
                    priority="normal",
                    subject=subject or "Email Support Request",
                )
                ticket = await ticket_crud.create(session, obj_in=ticket_data)
                
                # Step 4: Save incoming message
                message_data = MessageCreate(
                    conversation_id=conversation.id,
                    sender_type="customer",
                    channel="email",
                    content=body,
                    role="user",
                )
                message = await message_crud.create(session, obj_in=message_data)
                
                logger.info(f"✅ Ticket created: {ticket.id}")
                
                # Step 5: Send reply via email
                await gmail_service.send_email(
                    to=from_email,
                    subject=f"Re: {subject}",
                    body=f"""Dear {customer.name},

Thank you for contacting Customer Support!

I've received your email regarding: {subject}

I've created a support ticket (ID: {ticket.id}) and I'm reviewing your request. 
I'll get back to you with a detailed response shortly.

Best regards,
Customer Support Team
{to_email}
""",
                )
                
                logger.info(f"✅ Reply sent to {from_email}")
                
                # Step 6: Trigger AI auto-responder
                asyncio.create_task(
                    auto_responder_service.process_message(
                        session,
                        ticket_id=ticket.id,
                        message_text=body,
                        customer_email=from_email,
                        customer_phone=customer.phone,
                    )
                )
                
                break
                
        except Exception as e:
            logger.error(f"❌ Error handling email: {e}", exc_info=True)


# Singleton instance
gmail_polling_service = GmailPollingService()
