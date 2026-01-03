from services.similarity import compute_similarity

def detect_contradiction(snippets: list[str]) -> bool:
    if len(snippets) < 2:
        return False

    # Compare first snippet against others
    base = snippets[0]
    others = snippets[1:]

    similarity = compute_similarity(base, others)

    # Low similarity between sources = possible contradiction
    return similarity < 0.35
