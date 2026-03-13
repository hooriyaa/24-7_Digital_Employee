"""
UltraMsg WhatsApp Service.

Handles WhatsApp messaging via UltraMsg API.
Documentation: https://ultramsg.com/docs
"""
from typing import Optional

import httpx

from app.config import get_settings


class UltraMsgService:
    """
    Service for sending and receiving WhatsApp messages via UltraMsg.
    
    Features:
    - Send text messages
    - Send images/documents
    - Receive webhooks
    - Message status tracking
    """
    
    def __init__(self):
        """Initialize UltraMsg service."""
        settings = get_settings()
        self.instance_id = settings.ultramsg_instance_id
        self.token = settings.ultramsg_token
        self.base_url = f"https://api.ultramsg.com/{self.instance_id}/messages/chat"
        self.headers = {"Content-Type": "application/x-www-form-urlencoded"}
    
    async def send_message(
        self,
        phone: str,
        message: str,
    ) -> dict:
        """
        Send a WhatsApp message.
        
        Args:
            phone: Recipient phone number (with country code, e.g., +1234567890)
            message: Message text
            
        Returns:
            dict with sent status and message ID
            
        Raises:
            httpx.HTTPError: If API request fails
        """
        payload = {
            "token": self.token,
            "to": phone,
            "body": message,
            "priority": 1,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                self.base_url,
                data=payload,
                headers=self.headers,
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
            
            if result.get("sent") == "true":
                return {
                    "success": True,
                    "message_id": result.get("id"),
                    "status": "sent",
                }
            else:
                return {
                    "success": False,
                    "error": result.get("error"),
                }
    
    async def send_image(
        self,
        phone: str,
        image_url: str,
        caption: str = "",
    ) -> dict:
        """
        Send an image via WhatsApp.
        
        Args:
            phone: Recipient phone number
            image_url: URL of the image to send
            caption: Optional caption
            
        Returns:
            dict with sent status
        """
        payload = {
            "token": self.token,
            "to": phone,
            "image": image_url,
            "caption": caption,
            "priority": 1,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.ultramsg.com/{self.instance_id}/messages/image",
                data=payload,
                headers=self.headers,
                timeout=30.0,
            )
            response.raise_for_status()
            result = response.json()
            
            return {
                "success": result.get("sent") == "true",
                "message_id": result.get("id"),
            }
    
    async def get_status(self, message_id: str) -> dict:
        """
        Get message delivery status.
        
        Args:
            message_id: Message ID from send response
            
        Returns:
            dict with status information
        """
        payload = {
            "token": self.token,
            "id": message_id,
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://api.ultramsg.com/{self.instance_id}/messages/status",
                data=payload,
                headers=self.headers,
                timeout=30.0,
            )
            response.raise_for_status()
            return response.json()
    
    def verify_webhook(self, data: dict) -> bool:
        """
        Verify incoming webhook from UltraMsg.
        
        Args:
            data: Webhook payload
            
        Returns:
            True if webhook is valid
        """
        # UltraMsg webhooks include instance_id for verification
        return data.get("instanceId") == self.instance_id
    
    def parse_webhook_message(self, data: dict) -> Optional[dict]:
        """
        Parse incoming message from webhook.
        
        Args:
            data: Webhook payload
            
        Returns:
            dict with message details or None
        """
        if data.get("type") != "text":
            return None
        
        return {
            "from": data.get("from"),
            "message": data.get("body"),
            "timestamp": data.get("timestamp"),
            "type": "text",
        }


# Singleton instance
ultramsg_service = UltraMsgService()
