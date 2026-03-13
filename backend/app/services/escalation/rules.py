"""
Escalation Rules Service.

Determines when a ticket should be escalated to a human agent.
"""
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class EscalationReason(str, Enum):
    """Reasons for ticket escalation."""
    
    LOW_CONFIDENCE = "low_confidence"
    NEGATIVE_SENTIMENT = "negative_sentiment"
    CUSTOMER_REQUEST = "customer_request"
    COMPLEX_ISSUE = "complex_issue"
    PRICING_BILLING = "pricing_billing"
    VIP_CUSTOMER = "vip_customer"
    REPEATED_ISSUE = "repeated_issue"


class EscalationResult(BaseModel):
    """Result of escalation evaluation."""
    
    should_escalate: bool
    reason: Optional[EscalationReason] = None
    confidence: float = 0.0
    details: str = ""


class EscalationService:
    """
    Service for evaluating escalation rules.
    
    Rules:
    1. Low confidence (< 0.7)
    2. Negative sentiment (< -0.5)
    3. Customer requests human
    4. Pricing/billing keywords
    """
    
    # Thresholds
    CONFIDENCE_THRESHOLD = 0.7
    SENTIMENT_THRESHOLD = -0.5
    
    # Customer request phrases
    HUMAN_REQUEST_PHRASES = [
        "speak to human",
        "talk to human",
        "speak to person",
        "talk to person",
        "speak to manager",
        "talk to manager",
        "human agent",
        "real person",
        "actual person",
        "customer service",
        "support agent",
    ]
    
    # Pricing/billing keywords
    PRICING_KEYWORDS = [
        "price",
        "pricing",
        "cost",
        "charge",
        "fee",
        "payment",
        "pay",
        "bill",
        "billing",
        "invoice",
        "refund",
        "refund",
        "cancel",
        "subscription",
        "upgrade",
        "downgrade",
    ]
    
    def should_escalate(
        self,
        *,
        confidence_score: Optional[float] = None,
        sentiment_score: Optional[float] = None,
        message_text: str = "",
        is_vip: bool = False,
        ticket_count: int = 0,
    ) -> EscalationResult:
        """
        Evaluate if ticket should be escalated.
        
        Args:
            confidence_score: AI confidence (0.0 to 1.0)
            sentiment_score: Sentiment (-1.0 to 1.0)
            message_text: Customer message text
            is_vip: Whether customer is VIP
            ticket_count: Number of previous tickets
            
        Returns:
            EscalationResult with decision and reason
        """
        text_lower = message_text.lower()
        
        # Rule 1: Low confidence
        if confidence_score is not None and confidence_score < self.CONFIDENCE_THRESHOLD:
            return EscalationResult(
                should_escalate=True,
                reason=EscalationReason.LOW_CONFIDENCE,
                confidence=1.0 - confidence_score,
                details=f"Confidence {confidence_score:.2f} below threshold {self.CONFIDENCE_THRESHOLD}",
            )
        
        # Rule 2: Negative sentiment
        if sentiment_score is not None and sentiment_score < self.SENTIMENT_THRESHOLD:
            return EscalationResult(
                should_escalate=True,
                reason=EscalationReason.NEGATIVE_SENTIMENT,
                confidence=abs(sentiment_score),
                details=f"Sentiment {sentiment_score:.2f} below threshold {self.SENTIMENT_THRESHOLD}",
            )
        
        # Rule 3: Customer requests human
        for phrase in self.HUMAN_REQUEST_PHRASES:
            if phrase in text_lower:
                return EscalationResult(
                    should_escalate=True,
                    reason=EscalationReason.CUSTOMER_REQUEST,
                    confidence=0.95,
                    details=f"Customer requested human: '{phrase}'",
                )
        
        # Rule 4: Pricing/billing keywords
        for keyword in self.PRICING_KEYWORDS:
            if keyword in text_lower:
                return EscalationResult(
                    should_escalate=True,
                    reason=EscalationReason.PRICING_BILLING,
                    confidence=0.7,
                    details=f"Pricing/billing keyword detected: '{keyword}'",
                )
        
        # VIP customer - auto escalate complex issues
        if is_vip and ticket_count > 2:
            return EscalationResult(
                should_escalate=True,
                reason=EscalationReason.VIP_CUSTOMER,
                confidence=0.8,
                details=f"VIP customer with {ticket_count} previous tickets",
            )
        
        # Repeated issue (3+ tickets)
        if ticket_count >= 3:
            return EscalationResult(
                should_escalate=True,
                reason=EscalationReason.REPEATED_ISSUE,
                confidence=0.85,
                details=f"Customer has {ticket_count} previous tickets",
            )
        
        # No escalation needed
        return EscalationResult(
            should_escalate=False,
            reason=None,
            confidence=0.0,
            details="No escalation criteria met",
        )
    
    def get_escalation_reasons(self) -> list[str]:
        """Get list of all escalation reasons."""
        return [reason.value for reason in EscalationReason]


# Singleton instance
escalation_service = EscalationService()
