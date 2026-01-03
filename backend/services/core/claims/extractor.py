from services.core.claims.sentence_segmenter import smart_sentence_segment
from services.core.claims.sentiment_analyzer import is_factual_claim
import logging

logger = logging.getLogger(__name__)

def extract_claims(text: str) -> list[str]:
    """
    Extract factual claims from text using intelligent sentence segmentation.
    Filters out opinions, questions, and conversational phrases.
    """
    if not text or not text.strip():
        return []

    # Use smart sentence segmentation
    sentences = smart_sentence_segment(text)
    
    claims = []

    opinion_starters = (
        "i think",
        "i believe",
        "in my opinion",
        "we think",
        "you should",
        "it seems",
        "probably",
        "maybe",
        "perhaps",
        "i feel",
        "i guess",
        "i would say",
        "in my view",
        "personally",
    )

    for s in sentences:
        cleaned = s.strip()

        # Filter too short sentences
        if len(cleaned) < 20:
            continue

        lower = cleaned.lower()

        # Remove questions
        if cleaned.endswith("?") or lower.startswith(("what", "who", "where", "when", "why", "how")):
            continue

        # Remove opinions / subjective statements
        is_opinion = any(lower.startswith(starter) for starter in opinion_starters)
        if is_opinion:
            continue

        # Filter out common conversational phrases
        if lower.startswith(("hello", "hi", "thanks", "thank you", "please", "sorry", "hey")):
            continue

        # Filter out list items and bullet points
        if cleaned.startswith(("- ", "* ", "• ", "1. ", "2. ", "3. ")):
            # Still include if it's a substantial claim
            if len(cleaned) < 50:
                continue

        # Check if it's a factual claim worth verifying (sentiment analysis)
        # Make sentiment check less strict - only filter obvious non-factual content
        try:
            is_factual, reason = is_factual_claim(cleaned)
            if not is_factual and reason in ["Too emotional", "Highly emotional", "Conversational"]:
                logger.debug(f"Skipping non-factual claim: {reason} - {cleaned[:50]}...")
                continue
            # Allow through if sentiment check fails or is uncertain
        except Exception as e:
            logger.warning(f"Sentiment analysis failed for claim, allowing through: {e}")
            # If sentiment analysis fails, allow the claim through

        claims.append(cleaned)

    return claims