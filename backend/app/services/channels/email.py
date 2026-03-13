"""
Gmail Email Service.

Handles email sending and receiving via Gmail API.
"""
from typing import Optional, List
import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import httpx

from app.config import get_settings


class GmailService:
    """
    Service for sending and receiving emails via Gmail API.
    
    Features:
    - Send emails
    - Fetch emails
    - Parse email content
    - Handle attachments (future)
    """
    
    def __init__(self):
        """Initialize Gmail service."""
        settings = get_settings()
        self.api_key = settings.gmail_api_key
        self.client_id = settings.gmail_client_id
        self.client_secret = settings.gmail_client_secret
        # In production, these would come from OAuth flow
        self.access_token: Optional[str] = None
    
    def _get_headers(self) -> dict:
        """Get authorization headers."""
        return {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
        }
    
    async def send_email(
        self,
        to: str,
        subject: str,
        body: str,
        html: bool = False,
    ) -> dict:
        """
        Send an email via Gmail API.
        
        Args:
            to: Recipient email address
            subject: Email subject
            body: Email body text
            html: Whether body is HTML
            
        Returns:
            dict with sent status and message ID
        """
        # Create MIME message
        message = MIMEMultipart("alternative")
        message["to"] = to
        message["subject"] = subject
        
        # Add plain text and HTML versions
        if html:
            message.attach(MIMEText(body, "html"))
        else:
            message.attach(MIMEText(body, "plain"))
        
        # Encode message
        raw_message = base64.urlsafe_b64encode(
            message.as_bytes()
        ).decode("utf-8")
        
        # Send via Gmail API
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://gmail.googleapis.com/gmail/v1/users/me/messages/send",
                headers=self._get_headers(),
                json={"raw": raw_message},
                timeout=30.0,
            )
            
            if response.status_code == 200:
                result = response.json()
                return {
                    "success": True,
                    "message_id": result.get("id"),
                    "thread_id": result.get("threadId"),
                }
            else:
                return {
                    "success": False,
                    "error": response.json().get("error", {}).get("message"),
                }
    
    async def fetch_emails(
        self,
        query: str = "is:unread",
        max_results: int = 10,
    ) -> List[dict]:
        """
        Fetch emails from Gmail.
        
        Args:
            query: Gmail search query
            max_results: Maximum number of emails to fetch
            
        Returns:
            List of email dictionaries
        """
        async with httpx.AsyncClient() as client:
            # List messages
            response = await client.get(
                "https://gmail.googleapis.com/gmail/v1/users/me/messages",
                headers=self._get_headers(),
                params={
                    "q": query,
                    "maxResults": max_results,
                },
                timeout=30.0,
            )
            
            if response.status_code != 200:
                return []
            
            messages = response.json().get("messages", [])
            
            # Fetch full message details
            emails = []
            for msg in messages[:max_results]:
                msg_detail = await self._get_message(client, msg["id"])
                if msg_detail:
                    emails.append(msg_detail)
            
            return emails
    
    async def _get_message(
        self,
        client: httpx.AsyncClient,
        message_id: str,
    ) -> Optional[dict]:
        """Get full message details."""
        response = await client.get(
            f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}",
            headers=self._get_headers(),
            params={"format": "full"},
            timeout=30.0,
        )
        
        if response.status_code != 200:
            return None
        
        msg_data = response.json()
        payload = msg_data.get("payload", {})
        headers = {h["name"]: h["value"] for h in payload.get("headers", [])}
        
        # Get body content
        body = ""
        if "parts" in payload:
            for part in payload["parts"]:
                if part["mimeType"] == "text/plain":
                    body = base64.urlsafe_b64decode(
                        part["body"]["data"]
                    ).decode("utf-8")
                    break
        elif "body" in payload and "data" in payload["body"]:
            body = base64.urlsafe_b64decode(
                payload["body"]["data"]
            ).decode("utf-8")
        
        return {
            "id": msg_data["id"],
            "thread_id": msg_data["threadId"],
            "from": headers.get("From", ""),
            "to": headers.get("To", ""),
            "subject": headers.get("Subject", ""),
            "date": headers.get("Date", ""),
            "body": body,
            "snippet": msg_data.get("snippet", ""),
        }
    
    async def mark_as_read(self, message_id: str) -> bool:
        """Mark an email as read."""
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"https://gmail.googleapis.com/gmail/v1/users/me/messages/{message_id}/modify",
                headers=self._get_headers(),
                json={"removeLabelIds": ["UNREAD"]},
                timeout=30.0,
            )
            return response.status_code == 200
    
    def parse_incoming_email(self, email_data: dict) -> dict:
        """
        Parse incoming email for ticket creation.
        
        Args:
            email_data: Email data from fetch
            
        Returns:
            dict with parsed email details
        """
        return {
            "from": email_data.get("from", ""),
            "subject": email_data.get("subject", ""),
            "body": email_data.get("body", ""),
            "date": email_data.get("date", ""),
            "message_id": email_data.get("id", ""),
            "thread_id": email_data.get("thread_id", ""),
        }


# Singleton instance
gmail_service = GmailService()
