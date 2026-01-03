from sentence_transformers import util
from services.core.verification.model_registry import get_embedding_model

def compute_similarity(
    claim: str,
    sources: list[str],
    domain: str
) -> float:
    """
    Compute semantic similarity using pretrained domain-specific model.
    CPU-only for stability and compatibility.
    """
    if not sources:
        return 0.0

    model = get_embedding_model(domain)
    
    try:
        # CPU-only encoding for stability
        claim_embedding = model.encode(claim, convert_to_tensor=True, show_progress_bar=False)
        source_embeddings = model.encode(sources, convert_to_tensor=True, show_progress_bar=False, batch_size=16)
        
        similarities = util.cos_sim(claim_embedding, source_embeddings)
        max_similarity = float(similarities.max().item())
        
        return max_similarity
    except Exception:
        # Fallback with CPU
        claim_embedding = model.encode(claim, convert_to_tensor=True, show_progress_bar=False)
        source_embeddings = model.encode(sources, convert_to_tensor=True, show_progress_bar=False)
        similarities = util.cos_sim(claim_embedding, source_embeddings)
        return float(similarities.max().item())
