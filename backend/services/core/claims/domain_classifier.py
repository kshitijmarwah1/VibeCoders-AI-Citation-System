import logging

logger = logging.getLogger(__name__)

# Domain keyword patterns with weights
DOMAIN_KEYWORDS = {
    "medical": {
        "keywords": [
            "disease", "treatment", "patient", "clinical", "diagnosis", "symptom",
            "medication", "therapy", "surgery", "hospital", "doctor", "physician",
            "cancer", "infection", "virus", "bacteria", "vaccine", "immune",
            "cardiac", "respiratory", "neurological", "pharmaceutical"
        ],
        "weight": 1.0
    },
    "finance": {
        "keywords": [
            "stock", "market", "revenue", "profit", "investment", "portfolio",
            "dividend", "equity", "bond", "trading", "financial", "bank",
            "currency", "exchange", "economy", "inflation", "debt", "asset",
            "securities", "hedge fund", "mutual fund", "ipo"
        ],
        "weight": 1.0
    },
    "legal": {
        "keywords": [
            "law", "court", "constitution", "act", "statute", "legal",
            "attorney", "lawyer", "judge", "lawsuit", "litigation", "contract",
            "jurisdiction", "precedent", "appeal", "verdict", "plaintiff", "defendant",
            "supreme court", "federal", "state law", "criminal", "civil"
        ],
        "weight": 1.0
    },
    "technology": {
        "keywords": [
            "software", "ai", "algorithm", "computer", "programming", "code",
            "machine learning", "neural network", "data", "database", "server",
            "cloud", "api", "framework", "application", "system", "network",
            "cybersecurity", "blockchain", "cryptocurrency", "iot", "quantum"
        ],
        "weight": 1.0
    },
    "science": {
        "keywords": [
            "physics", "chemistry", "biology", "research", "experiment", "hypothesis",
            "theory", "molecule", "atom", "quantum", "genetic", "evolution",
            "laboratory", "scientist", "discovery", "publication", "journal",
            "peer review", "data analysis", "observation"
        ],
        "weight": 1.0
    }
}

def ml_detect_domain(text: str) -> tuple[str, float]:
    """
    Domain detection using keyword matching with improved heuristics.
    Returns: (domain, confidence)
    """
    if not text or not text.strip():
        return "general", 0.0

    # Limit text length for performance
    text = text[:1000]
    lowered = text.lower()

    # Score each domain based on keyword matches
    domain_scores = {}
    
    for domain, config in DOMAIN_KEYWORDS.items():
        score = 0.0
        keywords = config["keywords"]
        weight = config["weight"]
        
        for keyword in keywords:
            # Count occurrences (case-insensitive)
            count = lowered.count(keyword.lower())
            if count > 0:
                # Weight by frequency (log scale to prevent over-weighting)
                score += weight * (1 + 0.5 * min(count, 3))
        
        domain_scores[domain] = score

    # Find best domain
    if not domain_scores or max(domain_scores.values()) == 0:
        return "general", 0.3

    best_domain = max(domain_scores, key=domain_scores.get)
    best_score = domain_scores[best_domain]

    # Normalize confidence (0.4 to 1.0 range)
    # Base confidence on relative score strength
    max_possible_score = len(DOMAIN_KEYWORDS[best_domain]["keywords"]) * 1.5
    confidence = min(best_score / max_possible_score, 1.0)
    confidence = max(0.4, confidence)  # Minimum 0.4 if domain detected

    # If confidence is too low, fallback to general
    if confidence < 0.4:
        return "general", 0.3

    return best_domain, round(confidence, 2)
