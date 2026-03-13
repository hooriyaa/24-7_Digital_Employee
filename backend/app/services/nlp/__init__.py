"""
NLP services exports.
"""
from app.services.nlp.sentiment import sentiment_service, SentimentService

__all__ = [
    "sentiment_service",
    "SentimentService",
]
