from collections import OrderedDict
import logging

logger = logging.getLogger(__name__)

# LRU Cache with size limit (max 1000 entries)
MAX_CACHE_SIZE = 1000
CACHE = OrderedDict()

def get_cached(key: str):
    """
    Get cached result. Moves item to end (most recently used).
    """
    if key in CACHE:
        # Move to end (most recently used)
        CACHE.move_to_end(key)
        return CACHE[key].copy()  # Return copy to prevent mutation
    return None

def set_cache(key: str, value: dict):
    """
    Set cache entry. Evicts oldest if cache is full.
    """
    try:
        if key in CACHE:
            # Update existing entry
            CACHE.move_to_end(key)
        else:
            # Add new entry
            if len(CACHE) >= MAX_CACHE_SIZE:
                # Evict oldest (first item)
                CACHE.popitem(last=False)
        
        CACHE[key] = value.copy()  # Store copy to prevent mutation
    except Exception as e:
        logger.warning(f"Cache write failed: {e}")

def clear_cache():
    """Clear all cache entries."""
    CACHE.clear()
