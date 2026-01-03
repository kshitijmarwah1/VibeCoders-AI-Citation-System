from services.domain_score import get_domain_weight

def calculate_credibility(citations: list[dict]) -> float:
    if not citations:
        return 0.0

    scores = []

    for cite in citations:
        url = cite.get("url", "")
        scores.append(get_domain_weight(url))

    return round(sum(scores) / len(scores), 2)
