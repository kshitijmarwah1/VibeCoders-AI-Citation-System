from services.core.scoring.domain import get_domain_weight
from services.config.domain_loader import load_domain_config

def calculate_credibility(citations: list[dict], domain: str = "general") -> float:
    """
    Calculate credibility score using domain-specific weights from YAML config.
    """
    if not citations:
        return 0.0

    try:
        domain_cfg = load_domain_config(domain)
        credibility_weights = domain_cfg.get("credibility_weights", {})
        default_weight = credibility_weights.get("default", 0.4)
    except Exception:
        credibility_weights = {}
        default_weight = 0.4

    scores = []

    for cite in citations:
        url = cite.get("url", "")
        # Use domain-specific weight if available, otherwise fallback to get_domain_weight
        weight = get_domain_weight(url, credibility_weights, default_weight)
        scores.append(weight)

    if not scores:
        return 0.0
    
    # Calculate average with minimum boost for having any citations
    avg_score = sum(scores) / len(scores)
    
    # Boost credibility if we have multiple sources (diversity bonus)
    if len(scores) >= 3:
        avg_score = min(avg_score * 1.1, 1.0)  # 10% boost for multiple sources
    elif len(scores) >= 2:
        avg_score = min(avg_score * 1.05, 1.0)  # 5% boost for 2 sources
    
    # Minimum credibility boost for having any citations
    if avg_score < 0.5 and len(scores) > 0:
        avg_score = max(avg_score, 0.5)  # At least 0.5 if we have citations
    
    return round(avg_score, 2)
