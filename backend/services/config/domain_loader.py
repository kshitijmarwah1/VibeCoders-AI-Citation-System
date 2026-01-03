import yaml
import os

BASE_PATH = os.path.dirname(__file__)
DOMAIN_PATH = os.path.join(BASE_PATH, "domains")

_DOMAIN_CACHE = {}

def load_domain_config(domain: str):
    """
    Loads and caches domain YAML config
    """
    if domain in _DOMAIN_CACHE:
        return _DOMAIN_CACHE[domain]

    file_path = os.path.join(DOMAIN_PATH, f"{domain}.yaml")

    if not os.path.exists(file_path):
        # fallback to general domain
        file_path = os.path.join(DOMAIN_PATH, "general.yaml")

    with open(file_path, "r", encoding="utf-8") as f:
        config = yaml.safe_load(f)

    _DOMAIN_CACHE[domain] = config
    return config
