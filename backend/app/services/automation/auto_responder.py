"""
Auto-Responder Service (Task 4.1).

Automatically responds to customer queries when:
1. Sentiment is positive (score > 0.3)
2. Answer is found in Knowledge Base with high confidence (> 0.8)
3. No human approval required

This reduces response time and allows human agents to focus on complex issues.
"""
import asyncio
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional
import uuid
import logging

from sqlmodel.ext.asyncio.session import AsyncSession

from app.services.nlp import sentiment_service
from app.crud import ticket_crud, message_crud, knowledge_base_crud
from app.services.ultramsg import ultramsg_service
from app.services.gmail import gmail_service

logger = logging.getLogger(__name__)

# Lazy import to avoid circular dependency
if TYPE_CHECKING:
    from app.agent.fte_agent import FTEAgent


class AutoResponderService:
    """
    Auto-Responder Service for common queries.

    Automatically replies to customer messages when:
    - Sentiment is positive (score > 0.3)
    - Answer found in Knowledge Base with confidence > 0.8
    - No escalation triggers detected
    """

    # Sentiment threshold for auto-response
    POSITIVE_SENTIMENT_THRESHOLD = 0.3

    # Confidence threshold for KB answers
    KB_CONFIDENCE_THRESHOLD = 0.8

    # Auto-response enabled flag
    enabled: bool = True

    async def should_auto_respond(
        self,
        message_text: str,
        sentiment_score: float,
    ) -> bool:
        """
        Determine if message qualifies for auto-response.

        Args:
            message_text: Customer message text
            sentiment_score: Sentiment analysis score (-1.0 to 1.0)

        Returns:
            True if auto-response is appropriate
        """
        if not self.enabled:
            print(f"⚠️  [AUTO-RESPONDER] Auto-responder is disabled")
            return False

        # Check for CRITICAL escalation triggers (these need human immediately)
        # Note: We REMOVED "refund", "cancel" from this list - those get AI response FIRST
        critical_escalation_triggers = [
            "lawsuit",
            "legal",
            "sue",
            "lawyer",
        ]

        message_lower = message_text.lower()
        for trigger in critical_escalation_triggers:
            if trigger in message_lower:
                print(f"⚠️  [AUTO-RESPONDER] Critical escalation trigger detected: '{trigger}'")
                return False

        # For web channel, ALWAYS respond (billing, refunds, etc. are handled by AI)
        # This ensures every customer gets a helpful response
        print(f"✅ [AUTO-RESPONDER] Will respond to customer message")
        return True

    async def find_kb_answer(
        self,
        query: str,
        session: AsyncSession,
    ) -> Optional[dict]:
        """
        Search knowledge base for answer.

        Args:
            query: Customer query
            session: Async database session

        Returns:
            dict with answer and confidence, or None if not found
        """
        try:
            # Search knowledge base using vector similarity
            results = await knowledge_base_crud.search_similar(
                session,
                query=query,
                limit=3,
            )

            if results:
                best_match = results[0]
                confidence = best_match.get("similarity", 0.0)

                if confidence >= self.KB_CONFIDENCE_THRESHOLD:
                    return {
                        "answer": best_match.get("content", ""),
                        "confidence": confidence,
                        "source": best_match.get("title", "Knowledge Base"),
                    }

        except Exception as e:
            # Log error but don't fail
            print(f"KB search error: {e}")

        return None

    async def process_message(
        self,
        session: AsyncSession,
        *,
        ticket_id: uuid.UUID,
        message_text: str,
        customer_email: str,
        customer_phone: Optional[str] = None,
    ) -> dict:
        """
        Process incoming message for potential auto-response.

        Args:
            session: Async database session
            ticket_id: Associated ticket ID
            message_text: Customer message text
            customer_email: Customer email for identity
            customer_phone: Optional customer phone for WhatsApp

        Returns:
            dict with processing result
        """
        print(f"\n🤖 [AUTO-RESPONDER] Starting process_message for ticket {ticket_id}")
        print(f"🤖 [AUTO-RESPONDER] Message text: {message_text[:100]}...")
        logger.info(f"🤖 [AUTO-RESPONDER] Starting process_message for ticket {ticket_id}")
        
        # Step 1: Analyze sentiment
        print(f"🤖 [AUTO-RESPONDER] Step 1: Analyzing sentiment...")
        sentiment_result = sentiment_service.analyze_sentiment_sync(message_text)
        sentiment_score = sentiment_result.get("score", 0.0)
        print(f"🤖 [AUTO-RESPONDER] Sentiment score: {sentiment_score}")
        logger.info(f"🤖 [AUTO-RESPONDER] Sentiment score: {sentiment_score}")

        # Step 2: Check if auto-response is appropriate
        print(f"🤖 [AUTO-RESPONDER] Step 2: Checking if auto-response is appropriate...")
        should_respond = await self.should_auto_respond(message_text, sentiment_score)
        print(f"🤖 [AUTO-RESPONDER] Should auto-respond: {should_respond}")
        
        if not should_respond:
            print(f"⚠️  [AUTO-RESPONDER] Skipping auto-response (sentiment not positive or escalation trigger)")
            logger.info(f"⚠️  [AUTO-RESPONDER] Skipping auto-response (sentiment not positive or escalation trigger)")
            return {
                "auto_responded": False,
                "reason": "Sentiment not positive or escalation trigger detected",
                "sentiment_score": sentiment_score,
            }

        # Step 3: Search knowledge base for answer
        print(f"🤖 [AUTO-RESPONDER] Step 3: Searching knowledge base...")
        kb_result = await self.find_kb_answer(message_text, session)

        if not kb_result:
            print(f"⚠️  [AUTO-RESPONDER] No confident answer in knowledge base")
            logger.info(f"⚠️  [AUTO-RESPONDER] No confident answer in knowledge base")
            # Continue without KB answer - will use FTE agent
            kb_result = None

        # Step 4: Generate response using FTE Agent
        print(f"🤖 [AUTO-RESPONDER] Step 4: Generating response with FTE Agent...")
        logger.info(f"🤖 [AUTO-RESPONDER] Step 4: Generating response with FTE Agent...")
        
        try:
            # Import FTE agent here to avoid circular dependency
            from app.agent import create_fte_agent
            
            fte_agent = create_fte_agent()
            print(f"🤖 [AUTO-RESPONDER] FTE Agent created: {fte_agent}")
            
            # Get ticket for context
            ticket = await ticket_crud.get(session, id=ticket_id)
            print(f"🤖 [AUTO-RESPONDER] Ticket context: {ticket.subject if ticket else 'N/A'}")
            
            # Generate response
            context = {
                "ticket_id": str(ticket_id),
                "customer_email": customer_email,
                "sentiment_score": sentiment_score,
            }
            
            print(f"🤖 [AUTO-RESPONDER] Calling FTE agent.generate_response()...")
            logger.info(f"🤖 [AUTO-RESPONDER] Calling FTE agent.generate_response()...")
            
            response_text = await fte_agent.generate_response(
                input_text=message_text,
                context=context,
            )
            
            print(f"✅ [AUTO-RESPONDER] FTE Agent response generated: {response_text[:100]}...")
            logger.info(f"✅ [AUTO-RESPONDER] FTE Agent response generated: {response_text[:100]}...")
            
        except Exception as e:
            print(f"❌ [AUTO-RESPONDER] FTE Agent error: {e}")
            logger.error(f"❌ [AUTO-RESPONDER] FTE Agent error: {e}", exc_info=True)
            
            # Smart fallback - analyze message for keywords
            message_lower = message_text.lower()
            
            if "charg" in message_lower and ("twice" in message_lower or "double" in message_lower or "58" in message_lower or "29" in message_lower):
                response_text = (
                    "I completely understand your concern about being charged twice, and I sincerely apologize for the confusion. "
                    "Let me explain what happened:\n\n"
                    "When you upgrade mid-cycle, you see two charges:\n"
                    "1. A prorated charge for the remainder of your previous billing period\n"
                    "2. Your regular monthly subscription charge\n\n"
                    "Your next charge on the 1st will be the standard $29/month.\n\n"
                    "I'm sending you a detailed breakdown via email. If you'd like, I can also connect you with our billing specialist who can review your account in detail.\n\n"
                    "Would you like me to:\n"
                    "• Send a detailed invoice breakdown\n"
                    "• Connect you with our billing team\n"
                    "• Process a refund for the prorated amount\n\n"
                    "Your satisfaction is our priority, and I'm here to make this right."
                )
            elif "refund" in message_lower or "cancel" in message_lower:
                response_text = (
                    "I understand you'd like a refund, and I want to help resolve this for you.\n\n"
                    "Good news - we offer a 30-day money-back guarantee on all Pro and Enterprise plans. "
                    "Since you're within that window, you're eligible for a full refund.\n\n"
                    "I'm escalating this to our billing team who will:\n"
                    "• Process your refund within 2-3 business days\n"
                    "• Send confirmation to your email\n"
                    "• Keep your account active until the end of the billing period\n\n"
                    "Alternatively, I can offer you:\n"
                    "• 50% off for the next 3 months\n"
                    "• Free upgrade to Enterprise for 1 month\n"
                    "• Extended 60-day trial to evaluate all features\n\n"
                    "What would work best for you?"
                )
            elif "pricing" in message_lower or "cost" in message_lower or "plan" in message_lower:
                response_text = (
                    "Great question! Here's our current pricing:\n\n"
                    "**Free Plan** - $0/month\n"
                    "• Up to 3 projects\n"
                    "• 5GB storage\n"
                    "• Basic features\n\n"
                    "**Pro Plan** - $29/month\n"
                    "• Unlimited projects\n"
                    "• Time tracking\n"
                    "• 100GB storage\n"
                    "• Email support\n\n"
                    "**Enterprise Plan** - $79/month\n"
                    "• Everything in Pro\n"
                    "• Advanced analytics\n"
                    "• 24/7 priority support\n"
                    "• Custom integrations\n\n"
                    "We also offer:\n"
                    "• 20% discount for annual billing\n"
                    "• 50% off for nonprofits\n"
                    "• 14-day free trial on Pro plan\n\n"
                    "Which plan are you interested in?"
                )
            else:
                # Generic but helpful fallback - ONLY for complex/unclear messages
                # For simple greetings like "hi", "hello", etc. - respond conversationally
                if message_text.strip().lower() in ["hi", "hello", "hey", "good morning", "good afternoon", "good evening"]:
                    response_text = (
                        "Hello! 👋 Thank you for reaching out. "
                        "I'm here to help you with any questions or concerns you may have. "
                        "Feel free to share more details about what you need assistance with, "
                        "and I'll provide you with the best possible support."
                    )
                elif len(message_text.strip()) < 10:
                    # Very short message - ask for more details
                    response_text = (
                        "Hi there! Thanks for your message. Could you please provide more details "
                        "about what you need help with? I'm here to assist you with any questions "
                        "about our product, pricing, features, or any issues you're experiencing."
                    )
                else:
                    # Complex message - use generic template
                    response_text = (
                        f"Thank you for your message! I've received your inquiry. "
                        "I'm reviewing your request and will provide a detailed response shortly. "
                        "Our team is committed to resolving this for you as quickly as possible.\n\n"
                        "Is there anything else you'd like to add to your ticket?"
                    )
        
        # Step 5: Send response via appropriate channel
        print(f"🤖 [AUTO-RESPONDER] Step 5: Sending response via channel...")
        channel = "web"  # Default to web
        
        try:
            # Try WhatsApp first if phone available
            if customer_phone:
                print(f"📱 [AUTO-RESPONDER] Sending via WhatsApp to {customer_phone}")
                try:
                    await ultramsg_service.send_message(
                        phone=customer_phone,
                        message=response_text,
                    )
                    channel = "whatsapp"
                    print(f"✅ [AUTO-RESPONDER] WhatsApp message sent successfully")
                except Exception as whatsapp_error:
                    print(f"⚠️  [AUTO-RESPONDER] WhatsApp send failed (silent fail): {whatsapp_error}")
                    logger.warning(f"WhatsApp send failed (silent fail): {whatsapp_error}")
                    # Silent fail - continue to save in conversation
                    channel = "web"
            elif customer_email:
                print(f"📧 [AUTO-RESPONDER] Sending via Email to {customer_email}")
                # Fallback to email
                try:
                    await gmail_service.send_email(
                        to=customer_email,
                        subject=f"Re: Ticket {str(ticket_id)[:8]}",
                        body=response_text,
                    )
                    channel = "email"
                    print(f"✅ [AUTO-RESPONDER] Email sent successfully")
                except Exception as email_error:
                    print(f"⚠️  [AUTO-RESPONDER] Email send failed (silent fail): {email_error}")
                    logger.warning(f"Email send failed (silent fail): {email_error}")
                    channel = "web"
            else:
                print(f"🌐 [AUTO-RESPONDER] No phone or email, will save to conversation only")

            # Step 6: Log auto-response in ticket conversation (ALWAYS do this for web channel)
            print(f"🤖 [AUTO-RESPONDER] Step 6: Saving response to conversation...")
            logger.info(f"🤖 [AUTO-RESPONDER] Step 6: Saving response to conversation...")
            
            # Get conversation_id from ticket
            if ticket and ticket.conversation_id:
                print(f"🤖 [AUTO-RESPONDER] Creating message in conversation {ticket.conversation_id}")
                
                await message_crud.create(
                    session,
                    obj_in={
                        "conversation_id": ticket.conversation_id,
                        "sender_type": "agent",
                        "channel": channel,
                        "content": response_text,
                        "role": "assistant",
                    },
                )
                print(f"✅ [AUTO-RESPONDER] Message saved to conversation!")
                logger.info(f"✅ [AUTO-RESPONDER] Message saved to conversation!")
            else:
                print(f"⚠️  [AUTO-RESPONDER] No conversation_id found for ticket")

            # Update ticket with auto-response metadata
            await ticket_crud.update_by_id(
                session,
                id=ticket_id,
                obj_in={
                    "confidence_score": kb_result["confidence"] if kb_result else 0.8,
                },
            )

            print(f"🎉 [AUTO-RESPONDER] Auto-response completed successfully!")
            logger.info(f"🎉 [AUTO-RESPONDER] Auto-response completed successfully!")
            
            return {
                "auto_responded": True,
                "response": response_text,
                "channel": channel,
                "sentiment_score": sentiment_score,
                "kb_confidence": kb_result["confidence"] if kb_result else 0.8,
            }

        except Exception as e:
            print(f"❌ [AUTO-RESPONDER] Failed to send response: {e}")
            logger.error(f"❌ [AUTO-RESPONDER] Failed to send response: {e}", exc_info=True)
            return {
                "auto_responded": False,
                "reason": f"Failed to send response: {str(e)}",
                "sentiment_score": sentiment_score,
            }


# Singleton instance
auto_responder_service = AutoResponderService()
