"""
Test Sentiment Analysis Service.
"""
import asyncio

from app.services.nlp import sentiment_service, SentimentService


def test_sentiment_imports():
    """Test that sentiment components can be imported."""
    print("Testing sentiment imports...")
    
    assert sentiment_service is not None
    assert SentimentService is not None
    
    print("  Sentiment imports: PASSED")
    return True


def test_sentiment_service_init():
    """Test sentiment service initialization."""
    print("\nTesting sentiment service initialization...")
    
    service = SentimentService()
    assert service is not None
    
    print("  Sentiment service init: PASSED")
    return True


async def test_positive_sentiment():
    """Test positive sentiment detection."""
    print("\nTesting positive sentiment...")
    
    text = "I'm very happy with your service! Thank you so much for the excellent support!"
    result = sentiment_service.analyze_sentiment_sync(text)
    
    assert "score" in result
    assert "emotion" in result
    assert "needs_escalation" in result
    
    print(f"  Text: {text[:50]}...")
    print(f"  Score: {result['score']}")
    print(f"  Emotion: {result['emotion']}")
    print(f"  Needs Escalation: {result['needs_escalation']}")
    
    # Score should be positive
    assert result['score'] > 0.3, f"Expected positive score, got {result['score']}"
    
    print("  Positive sentiment: PASSED")
    return result


async def test_negative_sentiment():
    """Test negative sentiment detection."""
    print("\nTesting negative sentiment...")
    
    text = "This is terrible! I'm very frustrated and angry with this service!"
    result = sentiment_service.analyze_sentiment_sync(text)
    
    assert "score" in result
    assert "emotion" in result
    assert "needs_escalation" in result
    
    print(f"  Text: {text[:50]}...")
    print(f"  Score: {result['score']}")
    print(f"  Emotion: {result['emotion']}")
    print(f"  Needs Escalation: {result['needs_escalation']}")
    
    # Score should be negative
    assert result['score'] < -0.3, f"Expected negative score, got {result['score']}"
    
    print("  Negative sentiment: PASSED")
    return result


async def test_neutral_sentiment():
    """Test neutral sentiment detection."""
    print("\nTesting neutral sentiment...")
    
    text = "I have a question about my account."
    result = sentiment_service.analyze_sentiment_sync(text)
    
    assert "score" in result
    assert "emotion" in result
    assert "needs_escalation" in result
    
    print(f"  Text: {text[:50]}...")
    print(f"  Score: {result['score']}")
    print(f"  Emotion: {result['emotion']}")
    print(f"  Needs Escalation: {result['needs_escalation']}")
    
    # Score should be near neutral
    assert -0.1 < result['score'] < 0.1, f"Expected neutral score, got {result['score']}"
    
    print("  Neutral sentiment: PASSED")
    return result


def test_escalation_logic():
    """Test escalation decision logic."""
    print("\nTesting escalation logic...")
    
    # Test with negative sentiment
    negative_result = {
        "score": -0.8,
        "emotion": "anger",
        "needs_escalation": True,
    }
    assert sentiment_service.should_escalate(negative_result) is True
    
    # Test with frustration
    frustrated_result = {
        "score": -0.3,
        "emotion": "frustration",
        "needs_escalation": False,
    }
    assert sentiment_service.should_escalate(frustrated_result) is True
    
    # Test with neutral
    neutral_result = {
        "score": 0.0,
        "emotion": "neutral",
        "needs_escalation": False,
    }
    assert sentiment_service.should_escalate(neutral_result) is False
    
    print("  Escalation logic: PASSED")
    return True


async def main():
    """Run all sentiment tests."""
    print("=" * 50)
    print("Sentiment Analysis Tests")
    print("=" * 50)
    
    try:
        test_sentiment_imports()
        test_sentiment_service_init()
        
        await test_positive_sentiment()
        await test_negative_sentiment()
        await test_neutral_sentiment()
        test_escalation_logic()
        
        print("\n" + "=" * 50)
        print("All Sentiment Tests PASSED!")
        print("=" * 50)
        
        return True
        
    except Exception as e:
        print(f"\nTest FAILED: {e}")
        print("=" * 50)
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = asyncio.run(main())
    exit(0 if success else 1)
