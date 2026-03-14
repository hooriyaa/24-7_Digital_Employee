"""
UltraMsg Service - WhatsApp messaging via UltraMsg API.
"""
import logging
import httpx
import os
from typing import Optional

logger = logging.getLogger(__name__)


class UltraMsgService:
    """
    UltraMsg API service for WhatsApp messaging.
    """
    
    def __init__(self):
        """Initialize UltraMsg service."""
        self.instance_id = os.getenv("ULTRAMSG_INSTANCE_ID", "")
        self.token = os.getenv("ULTRAMSG_TOKEN", "")
        self.base_url = "https://api.ultramsg.com"
        self.enabled = bool(self.instance_id and self.token)
        
    def verify_webhook(self, data: dict) -> bool:
        """
        Verify incoming webhook from UltraMsg.
        
        For now, accept all webhooks (add proper verification later)
        """
        return True
        
    async def send_message(
        self,
        phone: str,
        message: str,
    ) -> bool:
        """
        Send WhatsApp message via UltraMsg API.
        
        Args:
            phone: Recipient phone number (with country code)
            message: Message text
            
        Returns:
            True if sent successfully, False otherwise
        """
        if not self.enabled:
            logger.warning(f"UltraMsg not configured, logging message only")
            logger.info(f"📱 WhatsApp message to {phone}: {message[:100]}...")
            return True
            
        try:
            url = f"{self.base_url}/{self.instance_id}/messages/chat"
            
            payload = {
                "token": self.token,
                "to": phone,
                "body": message,
            }
            
            async with httpx.AsyncClient() as client:
                response = await client.post(url, data=payload)
                
                if response.status_code == 200:
                    logger.info(f"✅ WhatsApp sent to {phone}")
                    return True
                else:
                    logger.error(f"❌ UltraMsg API error: {response.status_code}")
                    return False
                    
        except Exception as e:
            logger.error(f"❌ Failed to send WhatsApp message: {e}", exc_info=True)
            return False


# Singleton instance
ultramsg_service = UltraMsgService()
