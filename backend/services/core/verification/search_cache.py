"""
Enhanced caching for web searches to reduce redundant Tavily API calls.
Uses semantic similarity to find similar cached searches.
"""
import logging
from typing import List, Dict, Tuple
from services.storage.cache import get_cached, set_cache
from services.core.verification.model_registry import get_embedding_model
from sentence_transformers import util

logger = logging.getLogger(__name__)

# Separate cache for search results (keyed by claim text)
_SEARCH_CACHE = {}

# Similarity threshold for reusing cached searches
SIMILARITY_THRESHOLD = 0.85

def _get_cached_search_similar(claim: str, domain: str = "general") -> Tuple[List[Dict], List[str]] | None:
    """
    Find a similar cached search result using semantic similarity.
    Returns cached (citations, snippets) if similar claim found, else None.
    """
    if not _SEARCH_CACHE:
        return None
    
    try:
        model = get_embedding_model(domain)
        
        claim_embedding = model.encode(claim, convert_to_tensor=True, show_progress_bar=False)
        
        best_match = None
        best_similarity = 0.0
        
        # Check all cached searches
        for cached_claim, cached_data in _SEARCH_CACHE.items():
            try:
                cached_embedding = model.encode(cached_claim, convert_to_tensor=True, show_progress_bar=False)
                similarity = float(util.cos_sim(claim_embedding, cached_embedding)[0][0].item())
                
                if similarity > best_similarity and similarity >= SIMILARITY_THRESHOLD:
                    best_similarity = similarity
                    best_match = cached_data
            except Exception as e:
                logger.warning(f"Error comparing with cached search: {e}")
                continue
        
        if best_match:
            logger.info(f"Reusing cached search (similarity: {best_similarity:.2f})")
            return best_match["citations"], best_match["snippets"]
        
        return None
    except Exception as e:
        logger.warning(f"Semantic search cache lookup failed: {e}")
        return None

def _cache_search_result(claim: str, citations: List[Dict], snippets: List[str]):
    """Cache search results for future use."""
    try:
        _SEARCH_CACHE[claim] = {
            "citations": citations,
            "snippets": snippets
        }
        
        # Limit cache size (keep most recent 500)
        if len(_SEARCH_CACHE) > 500:
            # Remove oldest entry (simple FIFO)
            oldest_key = next(iter(_SEARCH_CACHE))
            del _SEARCH_CACHE[oldest_key]
    except Exception as e:
        logger.warning(f"Failed to cache search result: {e}")

def get_cached_or_search(claim: str, domain: str = "general", search_func=None) -> Tuple[List[Dict], List[str]]:
    """
    Get search results from cache if similar claim exists, otherwise perform new search.
    
    Args:
        claim: The claim to search for
        domain: Domain for model selection
        search_func: Function to call if cache miss (should return (citations, snippets))
    
    Returns:
        (citations, snippets)
    """
    # First check exact match
    if claim in _SEARCH_CACHE:
        logger.info("Exact cache hit for search")
        cached = _SEARCH_CACHE[claim]
        return cached["citations"], cached["snippets"]
    
    # Check for similar claims
    similar_result = _get_cached_search_similar(claim, domain)
    if similar_result:
        return similar_result
    
    # Cache miss - perform new search
    if search_func:
        try:
            citations, snippets = search_func(claim)
            _cache_search_result(claim, citations, snippets)
            return citations, snippets
        except Exception as e:
            logger.error(f"Search function failed: {e}")
            return [], []
    
    return [], []

