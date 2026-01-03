CACHE = {}

def get_cached(key):
    return CACHE.get(key)

def set_cache(key, value):
    CACHE[key] = value
