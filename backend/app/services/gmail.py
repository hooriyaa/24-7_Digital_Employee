"""
Gmail Service - Send emails via Gmail API or SMTP.
"""
import logging
import smtplib
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

logger = logging.getLogger(__name__)


class GmailService:
    """
    Gmail API service for sending emails.
    """
    
    def __init__(self):
        """Initialize Gmail service."""
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        self.sender_email = os.getenv("GMAIL_SENDER_EMAIL", "support@example.com")
        self.sender_password = os.getenv("GMAIL_SENDER_PASSWORD", "")
        
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
    ) -> bool:
        """
        Send an email via Gmail SMTP.

        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body content
            html: Whether body is HTML (default: False)
            
        Returns:
            True if sent successfully, False otherwise
        """
        try:
            logger.info(f"📧 Sending email to: {to}")
            logger.info(f"📝 Subject: {subject}")
            logger.info(f"📄 Body: {body[:100]}...")
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.sender_email
            msg['To'] = to
            msg['Subject'] = subject
            
            # Attach body
            msg.attach(MIMEText(body, 'html' if html else 'plain', 'utf-8'))
            
            # Send via SMTP (if credentials are configured)
            if self.sender_password:
                with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                    server.starttls()
                    server.login(self.sender_email, self.sender_password)
                    server.send_message(msg)
                logger.info(f"✅ Email sent successfully to {to} via SMTP")
            else:
                # No credentials - just log (development mode)
                logger.info(f"✅ [DEV MODE] Email would be sent to {to}")
                logger.info(f"   From: {self.sender_email}")
                logger.info(f"   Subject: {subject}")
            
            return True
            
        except Exception as e:
            logger.error(f"❌ Failed to send email: {e}", exc_info=True)
            return False


# Singleton instance
gmail_service = GmailService()
