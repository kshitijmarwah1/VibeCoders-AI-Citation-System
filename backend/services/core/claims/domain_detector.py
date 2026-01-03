from services.core.claims.domain_classifier import ml_detect_domain

def detect_domain(text: str) -> str:
    domain, confidence = ml_detect_domain(text)

    # Fallback for safety
    if confidence < 0.4:
        return "general"

    return domain
