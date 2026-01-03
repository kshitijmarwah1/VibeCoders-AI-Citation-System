"""
Sentiment and content type analysis for filtering claims.
Detects emotional, conversational, and factual content.
"""
import logging
from typing import Dict, Tuple
from transformers import pipeline

logger = logging.getLogger(__name__)

# Lazy loading for sentiment pipeline
_sentiment_pipeline = None
_emotion_pipeline = None

def _get_sentiment_pipeline():
    """Lazy load sentiment analysis pipeline."""
    global _sentiment_pipeline
    if _sentiment_pipeline is None:
        try:
            _sentiment_pipeline = pipeline(
                "sentiment-analysis",
                model="cardiffnlp/twitter-roberta-base-sentiment-latest",
                top_k=None  # Use top_k instead of deprecated return_all_scores
            )
        except Exception as e:
            logger.warning(f"Failed to load sentiment model: {e}")
            return None
    return _sentiment_pipeline

def analyze_sentiment(text: str) -> Dict[str, float]:
    """
    Analyze sentiment of text.
    Returns: {"positive": 0.0-1.0, "negative": 0.0-1.0, "neutral": 0.0-1.0}
    """
    if not text or len(text.strip()) < 10:
        return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
    
    pipeline = _get_sentiment_pipeline()
    if pipeline is None:
        return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}
    
    try:
        # Limit text length for performance
        text_short = text[:512]
        results = pipeline(text_short)
        
        # Map results to our format
        sentiment_scores = {"positive": 0.0, "negative": 0.0, "neutral": 0.0}
        
        for result in results[0]:
            label = result["label"].lower()
            score = result["score"]
            
            if "positive" in label:
                sentiment_scores["positive"] = score
            elif "negative" in label:
                sentiment_scores["negative"] = score
            elif "neutral" in label:
                sentiment_scores["neutral"] = score
        
        return sentiment_scores
    except Exception as e:
        logger.warning(f"Sentiment analysis failed: {e}")
        return {"positive": 0.0, "negative": 0.0, "neutral": 1.0}

def is_factual_claim(text: str) -> Tuple[bool, str]:
    """
    Determine if text is a factual claim worth verifying.
    Returns: (is_factual, reason)
    """
    if not text or len(text.strip()) < 20:
        return False, "Too short"
    
    text_lower = text.lower()
    
    # Emotional indicators
    emotional_words = [
        "feel", "feeling", "emotion", "love", "hate", "angry", "sad", "happy",
        "excited", "disappointed", "frustrated", "worried", "anxious", "scared"
    ]
    
    # Conversational indicators
    conversational_phrases = [
        "how are you", "what's up", "nice to meet", "talk to you later",
        "have a good day", "take care", "see you", "thanks for"
    ]
    
    # Opinion indicators
    opinion_indicators = [
        "i think", "i believe", "in my opinion", "i feel", "i guess",
        "probably", "maybe", "perhaps", "might be", "could be"
    ]
    
    # Check for emotional content
    emotional_count = sum(1 for word in emotional_words if word in text_lower)
    if emotional_count >= 2:
        return False, "Too emotional"
    
    # Check for conversational content
    if any(phrase in text_lower for phrase in conversational_phrases):
        return False, "Conversational"
    
    # Check for strong opinion indicators
    if any(indicator in text_lower for indicator in opinion_indicators):
        return False, "Opinion-based"
    
    # Analyze sentiment
    sentiment = analyze_sentiment(text)
    
    # If very emotional (high positive/negative, low neutral), likely not factual
    # But be less strict - only filter if extremely emotional
    if sentiment["neutral"] < 0.2 and (sentiment["positive"] > 0.8 or sentiment["negative"] > 0.8):
        return False, "Highly emotional"
    
    # Factual indicators
    factual_indicators = [
        "according to", "research shows", "studies indicate", "data suggests",
        "evidence", "proven", "established", "fact", "statistics", "percentage",
        "increased", "decreased", "found that", "discovered", "published"
    ]
    
    factual_count = sum(1 for indicator in factual_indicators if indicator in text_lower)
    
    # If has factual indicators and neutral sentiment, likely factual
    if factual_count >= 1 and sentiment["neutral"] > 0.5:
        return True, "Factual"
    
    # Default: if neutral sentiment and no strong emotional/conversational markers, consider factual
    if sentiment["neutral"] > 0.6:
        return True, "Neutral factual"
    
    return False, "Not clearly factual"

