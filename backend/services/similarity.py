from sentence_transformers import SentenceTransformer, util

# Load once (VERY IMPORTANT)
model = SentenceTransformer("all-MiniLM-L6-v2")

def compute_similarity(claim: str, sources: list[str]) -> float:
    """
    Returns max semantic similarity score between claim and sources
    """
    if not sources:
        return 0.0

    claim_embedding = model.encode(claim, convert_to_tensor=True)
    source_embeddings = model.encode(sources, convert_to_tensor=True)

    similarities = util.cos_sim(claim_embedding, source_embeddings)

    return float(similarities.max())
