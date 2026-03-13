"""
Sentiment Analysis Service.

Uses rule-based analysis with keyword matching for sentiment detection.
Returns score between -1.0 (very angry) and 1.0 (very happy).
"""
import re
from typing import Optional


class SentimentService:
    """
    Sentiment analysis service using rule-based approach.
    
    Analyzes customer messages and returns:
    - score: float between -1.0 (very negative) and 1.0 (very positive)
    - emotion: primary emotion detected
    - needs_escalation: boolean indicating if human escalation is recommended
    """
    
    # Negative keywords with intensity scores
    NEGATIVE_WORDS = {
        # Very negative (-1.0)
        "terrible": -1.0,
        "awful": -1.0,
        "horrible": -1.0,
        "hate": -1.0,
        "useless": -0.9,
        "worthless": -0.9,
        
        # Angry/frustrated (-0.7 to -0.9)
        "angry": -0.9,
        "furious": -0.9,
        "frustrated": -0.8,
        "annoyed": -0.7,
        "irritated": -0.7,
        
        # Disappointed (-0.5 to -0.7)
        "disappointed": -0.6,
        "unhappy": -0.6,
        "dissatisfied": -0.7,
        "poor": -0.5,
        "bad": -0.5,
        
        # Concern/negative (-0.3 to -0.5)
        "problem": -0.4,
        "issue": -0.3,
        "wrong": -0.4,
        "error": -0.3,
        "broken": -0.5,
        "fail": -0.5,
        "failed": -0.5,
    }
    
    # Positive keywords with intensity scores
    POSITIVE_WORDS = {
        # Very positive (1.0)
        "excellent": 1.0,
        "amazing": 1.0,
        "perfect": 1.0,
        "love": 0.95,
        "fantastic": 0.95,
        
        # Happy/satisfied (0.7 to 0.9)
        "happy": 0.8,
        "satisfied": 0.7,
        "pleased": 0.75,
        "great": 0.7,
        "wonderful": 0.85,
        
        # Appreciation (0.5 to 0.7)
        "thank": 0.6,
        "thanks": 0.6,
        "appreciate": 0.7,
        "helpful": 0.6,
        "good": 0.5,
        "nice": 0.5,
    }
    
    # Escalation trigger phrases
    ESCALATION_PHRASES = [
        "speak to human",
        "talk to human",
        "speak to person",
        "talk to person",
        "speak to manager",
        "talk to manager",
        "human agent",
        "real person",
        "customer service",
        "complaint",
        "refund",
        "cancel",
        "unsubscribe",
    ]
    
    def analyze_sentiment(self, text: str) -> dict:
        """
        Analyze sentiment of text using rule-based approach.
        
        Args:
            text: Text to analyze
            
        Returns:
            dict with score, emotion, and needs_escalation
        """
        if not text or not text.strip():
            return {
                "score": 0.0,
                "emotion": "neutral",
                "needs_escalation": False,
            }
        
        text_lower = text.lower()
        
        # Calculate sentiment score
        total_score = 0.0
        word_count = 0
        detected_emotions = []
        
        # Check for negative words
        for word, score in self.NEGATIVE_WORDS.items():
            if word in text_lower:
                total_score += score
                word_count += 1
                if score < -0.7:
                    detected_emotions.append("anger")
                elif score < -0.4:
                    detected_emotions.append("frustration")
                else:
                    detected_emotions.append("disappointment")
        
        # Check for positive words
        for word, score in self.POSITIVE_WORDS.items():
            if word in text_lower:
                total_score += score
                word_count += 1
                if score > 0.8:
                    detected_emotions.append("joy")
                elif score > 0.6:
                    detected_emotions.append("satisfaction")
                else:
                    detected_emotions.append("gratitude")
        
        # Normalize score to -1.0 to 1.0 range
        if word_count > 0:
            # Average score with intensity weighting
            score = total_score / word_count
            # Apply sigmoid-like scaling for more natural distribution
            score = max(-1.0, min(1.0, score))
        else:
            score = 0.0
        
        # Determine primary emotion
        if detected_emotions:
            emotion = max(set(detected_emotions), key=detected_emotions.count)
        else:
            emotion = "neutral"
        
        # Check for escalation triggers
        needs_escalation = False
        for phrase in self.ESCALATION_PHRASES:
            if phrase in text_lower:
                needs_escalation = True
                break
        
        # Also escalate if very negative
        if score < -0.5:
            needs_escalation = True
        
        return {
            "score": round(score, 2),
            "emotion": emotion,
            "needs_escalation": needs_escalation,
        }
    
    def analyze_sentiment_sync(self, text: str) -> dict:
        """
        Synchronous version of analyze_sentiment.
        
        Args:
            text: Text to analyze
            
        Returns:
            dict with score, emotion, and needs_escalation
        """
        return self.analyze_sentiment(text)
    
    def should_escalate(self, sentiment_result: dict) -> bool:
        """
        Determine if escalation is needed based on sentiment.
        
        Args:
            sentiment_result: Result from analyze_sentiment
            
        Returns:
            True if escalation recommended
        """
        score = sentiment_result.get("score", 0.0)
        needs_escalation = sentiment_result.get("needs_escalation", False)
        emotion = sentiment_result.get("emotion", "neutral")
        
        # Escalate if:
        # 1. Explicitly flagged by sentiment analysis
        # 2. Very negative score (< -0.5)
        # 3. Anger or frustration detected
        if needs_escalation:
            return True
        
        if score < -0.5:
            return True
        
        if emotion in ["anger", "frustration"]:
            return True
        
        return False


# Singleton instance
sentiment_service = SentimentService()
