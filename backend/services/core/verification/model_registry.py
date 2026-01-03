from sentence_transformers import SentenceTransformer
from services.config.domain_loader import load_domain_config
import logging

logger = logging.getLogger(__name__)

# Fallback registry (used if YAML doesn't specify embedding_model)
FALLBACK_MODEL_REGISTRY = {
    "general": "sentence-transformers/all-MiniLM-L6-v2",
    "medical": "pritamdeka/BioBERT-mnli-snli-scinli-scitail-mednli-stsb",
    "finance": "sentence-transformers/all-MiniLM-L6-v2",
    "legal": "sentence-transformers/all-MiniLM-L6-v2",
    "technology": "sentence-transformers/all-MiniLM-L6-v2",
    "science": "sentence-transformers/all-MiniLM-L6-v2",
}

_MODEL_CACHE = {}

def get_embedding_model(domain: str) -> SentenceTransformer:
    """
    Load and cache pretrained embedding models per domain.
    First tries to load from domain YAML config, falls back to registry.
    """
    try:
        domain_cfg = load_domain_config(domain)
        model_name = domain_cfg.get("embedding_model")
        
        if not model_name:
            # Fallback to registry
            model_name = FALLBACK_MODEL_REGISTRY.get(domain, FALLBACK_MODEL_REGISTRY["general"])
    except Exception as e:
        logger.warning(f"Failed to load domain config for {domain}, using fallback: {e}")
        model_name = FALLBACK_MODEL_REGISTRY.get(domain, FALLBACK_MODEL_REGISTRY["general"])

    if model_name not in _MODEL_CACHE:
        try:
            # CPU-only for stability
            model = SentenceTransformer(model_name, device='cpu')
            _MODEL_CACHE[model_name] = model
            logger.info(f"Loaded embedding model: {model_name} for domain: {domain}")
        except Exception as e:
            logger.error(f"Failed to load model {model_name}: {e}")
            # Fallback to general model
            fallback_model = FALLBACK_MODEL_REGISTRY["general"]
            if fallback_model not in _MODEL_CACHE:
                _MODEL_CACHE[fallback_model] = SentenceTransformer(fallback_model, device='cpu')
            return _MODEL_CACHE[fallback_model]

    return _MODEL_CACHE[model_name]
