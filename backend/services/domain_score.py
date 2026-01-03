from urllib.parse import urlparse

def get_domain_weight(url: str) -> float:
    domain = urlparse(url).netloc.lower()

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

    return 0.4
