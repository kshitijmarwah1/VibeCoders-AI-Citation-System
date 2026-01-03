from services.core.verification.semantic import compute_similarity

def detect_contradiction(
    snippets: list[str],
    domain: str,
    contradiction_threshold: float
) -> bool:
    """
    Detect contradictions by comparing semantic similarity between snippets.
    Low similarity between sources suggests contradiction.
    """
    if len(snippets) < 2:
        return False

    base = snippets[0]
    others = snippets[1:]

    # Compute similarity between base and each other snippet
    # If average similarity is below threshold, there's a contradiction
    similarities = []
    for other in others:
        try:
            sim = compute_similarity(base, [other], domain)
            similarities.append(sim)
        except Exception:
            continue

    if not similarities:
        return False

    avg_similarity = sum(similarities) / len(similarities)
    return avg_similarity < contradiction_threshold
