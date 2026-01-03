import logging
from services.core.verification.search import search_web_for_claim
from services.core.verification.semantic import compute_similarity
from services.core.verification.contradiction import detect_contradiction
from services.core.scoring.credibility import calculate_credibility
from services.storage.cache import get_cached, set_cache
from services.config.domain_loader import load_domain_config
from services.core.llm.reasoner import generate_explanation

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def verify_claim(claim: str, domain: str = "general") -> dict:
    """
    Verify a single claim by searching the web, computing similarity,
    checking credibility, and detecting contradictions.
    
    Returns:
        dict: Verification result with status, confidence, citations, etc.
        Must include: claim, status, confidence, similarity, credibility,
        contradicted, citations, explanation
    """
    try:
        domain_cfg = load_domain_config(domain)
        similarity_threshold = domain_cfg["similarity_threshold"]
        contradiction_penalty = domain_cfg["contradiction_penalty"]
        contradiction_threshold = domain_cfg.get("contradiction_threshold", 0.35)
    except Exception as e:
        logger.error(f"Failed to load domain config for {domain}: {e}")
        domain_cfg = load_domain_config("general")
        similarity_threshold = domain_cfg["similarity_threshold"]
        contradiction_penalty = domain_cfg["contradiction_penalty"]
        contradiction_threshold = domain_cfg.get("contradiction_threshold", 0.35)
        domain = "general"

    # Check cache first
    cached_result = get_cached(claim)
    if cached_result:
        # Ensure cached result has all required fields
        if "claim" not in cached_result:
            cached_result["claim"] = claim
        return cached_result

    # Search web for claim (with intelligent caching)
    try:
        citations, snippets = search_web_for_claim(claim, domain)
    except Exception as e:
        logger.error(f"Web search failed for claim: {claim[:50]}... Error: {e}")
        citations, snippets = [], []

    # Compute similarity
    try:
        similarity_score = compute_similarity(
            claim,
            snippets,
            domain
        )
    except Exception as e:
        logger.error(f"Similarity computation failed: {e}")
        similarity_score = 0.0

    # Calculate credibility (domain-aware)
    try:
        credibility_score = calculate_credibility(citations, domain)
    except Exception as e:
        logger.error(f"Credibility calculation failed: {e}")
        credibility_score = 0.0

    # Compute final score with improved formula
    # Weight similarity more heavily, but still consider credibility
    # If we have citations, boost the score slightly
    base_score = similarity_score * 0.7 + (similarity_score * credibility_score) * 0.3
    
    # Boost if we have multiple credible sources
    if len(citations) > 0:
        citation_boost = min(len(citations) * 0.05, 0.15)  # Max 15% boost
        base_score = min(base_score + citation_boost, 1.0)
    
    final_score = round(base_score, 2)
    
    # Detect contradictions
    has_contradiction = False
    try:
        if snippets and len(snippets) >= 2:
            has_contradiction = detect_contradiction(
                snippets,
                domain,
                contradiction_threshold
            )
            if has_contradiction:
                logger.warning(f"Contradiction detected for claim: {claim[:50]}...")
                final_score = round(final_score * contradiction_penalty, 2)
    except Exception as e:
        logger.error(f"Contradiction detection failed: {e}")

    # Determine verification status with adjusted threshold
    # Lower the threshold slightly if we have good citations
    adjusted_threshold = similarity_threshold
    if len(citations) >= 3 and credibility_score > 0.7:
        adjusted_threshold = similarity_threshold * 0.9  # 10% lower threshold
    
    status = "verified" if final_score >= adjusted_threshold else "hallucinated"
    
    # Generate explanation (for both verified and hallucinated)
    explanation = ""
    try:
        explanation = generate_explanation(
            claim=claim,
            status=status,
            confidence=final_score,
            citations=citations,
            similarity=similarity_score,
            credibility=credibility_score,
            contradicted=has_contradiction
        )
    except Exception as e:
        logger.warning(f"Explanation generation failed: {e}")
        explanation = f"Claim {status} with confidence {final_score:.2f} based on {len(citations)} sources."

    # Build result with all required fields
    result = {
        "claim": claim,
        "status": status,
        "confidence": final_score,
        "similarity": round(similarity_score, 2),
        "credibility": credibility_score,
        "contradicted": has_contradiction,
        "citations": citations,
        "explanation": explanation
    }
    
    # Cache result
    try:
        set_cache(claim, result)
    except Exception as e:
        logger.warning(f"Cache write failed: {e}")
    
    return result

