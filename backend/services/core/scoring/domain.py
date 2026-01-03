from urllib.parse import urlparse

def get_domain_weight(url: str, credibility_weights: dict = None, default_weight: float = 0.4) -> float:
    """
    Get credibility weight for a URL.
    First checks domain-specific YAML config, then falls back to hardcoded defaults.
    """
    if not url:
        return default_weight

    domain = urlparse(url).netloc.lower()
    
    # Remove www. prefix for matching
    if domain.startswith("www."):
        domain = domain[4:]

    # Check domain-specific weights from YAML first
    if credibility_weights:
        # Check exact domain match
        if domain in credibility_weights:
            return credibility_weights[domain]
        
        # Check partial matches (e.g., "wikipedia.org" matches "en.wikipedia.org")
        for trusted_domain, weight in credibility_weights.items():
            if trusted_domain != "default" and trusted_domain in domain:
                return weight

    # Fallback to hardcoded defaults (for backward compatibility)
    if "wikipedia.org" in domain:
        return 1.0

    if "britannica.com" in domain:
        return 0.95

    if domain.endswith(".gov") or domain.endswith(".edu"):
        return 0.95

    trusted_news = [
        "bbc.com",
        "reuters.com",
        "nytimes.com",
        "theguardian.com",
        "aljazeera.com"
    ]

    for site in trusted_news:
        if site in domain:
            return 0.85

    if "medium.com" in domain or "blog" in domain:
        return 0.6

    return default_weight
