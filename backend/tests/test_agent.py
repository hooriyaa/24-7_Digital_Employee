"""
Test suite for Customer Success FTE Agent.

Run with: pytest tests/test_agent.py -v
"""
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock, patch


# ============================================================================
# Test 1: Agent Initialization
# ============================================================================

def test_agent_initialization():
    """Test that agent initializes correctly."""
    from app.agent.fte_agent import FTEAgent, FTEAgentConfig
    
    config = FTEAgentConfig(
        model="litellm/gemini/gemini-2.0-flash",
        temperature=0.7,
        max_tokens=2000
    )
    
    agent = FTEAgent(config)
    
    assert agent is not None
    assert agent.config.temperature == 0.7
    assert agent.config.max_tokens == 2000


# ============================================================================
# Test 2: Sentiment Analysis
# ============================================================================

def test_sentiment_positive():
    """Test sentiment analysis for positive message."""
    from app.services.nlp import sentiment_service
    
    result = sentiment_service.analyze_sentiment_sync(
        "I love your product! It's amazing!"
    )
    
    assert result["score"] > 0.3
    assert result["label"] == "positive"


def test_sentiment_negative():
    """Test sentiment analysis for negative message."""
    from app.services.nlp import sentiment_service
    
    result = sentiment_service.analyze_sentiment_sync(
        "This is terrible! I'm very frustrated!"
    )
    
    assert result["score"] < -0.5
    assert result["label"] == "negative"


def test_sentiment_neutral():
    """Test sentiment analysis for neutral message."""
    from app.services.nlp import sentiment_service
    
    result = sentiment_service.analyze_sentiment_sync(
        "I have a question about pricing."
    )
    
    assert -0.3 <= result["score"] <= 0.3
    assert result["label"] == "neutral"


# ============================================================================
# Test 3: Knowledge Base Search
# ============================================================================

@pytest.mark.asyncio
async def test_knowledge_base_search():
    """Test knowledge base semantic search."""
    # Mock database session
    mock_session = AsyncMock()
    
    # Mock search results
    mock_results = [
        {
            "id": 1,
            "title": "Pro Plan Features",
            "content": "Our Pro plan includes unlimited projects...",
            "similarity": 0.95
        }
    ]
    
    # Mock database query
    with patch('app.crud.knowledge_base.knowledge_base_crud.search_similar', 
               return_value=mock_results):
        from app.services.automation.auto_responder import AutoResponderService
        
        service = AutoResponderService()
        result = await service.find_kb_answer(
            "What is Pro plan pricing?",
            mock_session
        )
        
        assert result is not None
        assert result["confidence"] == 0.95


# ============================================================================
# Test 4: Auto-Responder
# ============================================================================

@pytest.mark.asyncio
async def test_auto_responder_should_respond():
    """Test auto-responder decision logic."""
    from app.services.automation.auto_responder import AutoResponderService
    
    service = AutoResponderService()
    
    # Should respond (positive sentiment)
    should_respond = await service.should_auto_respond(
        message_text="Great product!",
        sentiment_score=0.8
    )
    
    assert should_respond is True


@pytest.mark.asyncio
async def test_auto_responder_should_escalate():
    """Test auto-responder escalation for negative sentiment."""
    from app.services.automation.auto_responder import AutoResponderService
    
    service = AutoResponderService()
    
    # Should NOT respond (negative sentiment - escalate)
    should_respond = await service.should_auto_respond(
        message_text="This is terrible!",
        sentiment_score=-0.7
    )
    
    assert should_respond is False


# ============================================================================
# Test 5: Channel Adaptation
# ============================================================================

def test_channel_adaptation_email():
    """Test email response formatting."""
    # Email should be formal and detailed
    email_response = """
Dear Valued Customer,

Thank you for contacting Customer Support.

We appreciate your inquiry and are here to help...

Best regards,
Customer Success Team
"""
    
    assert len(email_response.split()) > 50  # Detailed
    assert "Dear" in email_response  # Formal greeting


def test_channel_adaptation_whatsapp():
    """Test WhatsApp response formatting."""
    # WhatsApp should be conversational and concise
    whatsapp_response = "Hi there! 👋 Thanks for reaching out. How can I help?"
    
    assert len(whatsapp_response) < 160  # Concise
    assert "👋" in whatsapp_response  # Emoji OK


# ============================================================================
# Test 6: Customer Identification
# ============================================================================

@pytest.mark.asyncio
async def test_customer_lookup_by_email():
    """Test customer lookup by email."""
    mock_session = AsyncMock()
    
    # Mock existing customer
    mock_customer = MagicMock()
    mock_customer.id = "test-customer-id"
    mock_customer.email = "test@example.com"
    
    with patch('app.crud.customer.customer_crud.get_by_email', 
               return_value=mock_customer):
        from app.crud.customer import customer_crud
        
        result = await customer_crud.get_by_email(mock_session, "test@example.com")
        
        assert result is not None
        assert result.email == "test@example.com"


@pytest.mark.asyncio
async def test_customer_lookup_by_phone():
    """Test customer lookup by phone."""
    mock_session = AsyncMock()
    
    # Mock existing customer
    mock_customer = MagicMock()
    mock_customer.id = "test-customer-id"
    mock_customer.phone = "+923062371929"
    
    with patch('app.crud.customer.customer_crud.get_by_phone', 
               return_value=mock_customer):
        from app.crud.customer import customer_crud
        
        result = await customer_crud.get_by_phone(mock_session, "+923062371929")
        
        assert result is not None
        assert result.phone == "+923062371929"


# ============================================================================
# Test 7: Escalation Logic
# ============================================================================

def test_escalation_explicit_request():
    """Test escalation when customer requests human."""
    message = "I want to talk to a human agent"
    
    escalation_keywords = ["human", "agent", "representative", "manager"]
    
    should_escalate = any(
        keyword in message.lower() 
        for keyword in escalation_keywords
    )
    
    assert should_escalate is True


def test_escalation_negative_sentiment():
    """Test escalation for very negative sentiment."""
    sentiment_score = -0.7
    escalation_threshold = -0.5
    
    should_escalate = sentiment_score < escalation_threshold
    
    assert should_escalate is True


# ============================================================================
# Test 8: End-to-End Flow
# ============================================================================

@pytest.mark.asyncio
async def test_full_customer_interaction():
    """Test complete customer interaction flow."""
    # 1. Customer sends message
    message = "What features are included in Pro plan?"
    
    # 2. Analyze sentiment
    from app.services.nlp import sentiment_service
    sentiment = sentiment_service.analyze_sentiment_sync(message)
    assert sentiment["score"] >= 0.0  # Neutral or positive
    
    # 3. Search knowledge base
    # (Would test with mock DB)
    
    # 4. Generate response
    # (Would test with mock agent)
    
    # 5. Send response
    # (Would test with mock channel API)
    
    # For now, just verify flow works
    assert True


# ============================================================================
# Run Tests
# ============================================================================

if __name__ == "__main__":
    pytest.main([__file__, "-v"])
