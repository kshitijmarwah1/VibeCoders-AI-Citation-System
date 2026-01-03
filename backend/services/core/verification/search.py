from tavily import TavilyClient
from services.config.settings import TAVILY_API_KEY
from services.core.verification.search_cache import get_cached_or_search
import logging

logger = logging.getLogger(__name__)

# Initialize Tavily client (lazy loading to handle import errors)
_tavily_client = None

def _get_tavily_client():
    """Lazy load Tavily client."""
    global _tavily_client
    if _tavily_client is None:
        try:
            _tavily_client = TavilyClient(api_key=TAVILY_API_KEY)
        except Exception as e:
            logger.error(f"Failed to initialize Tavily client: {e}")
            return None
    return _tavily_client


def _perform_tavily_search(claim: str) -> tuple[list[dict], list[str]]:
    """
    Internal function to perform actual Tavily search.
    
    Returns:
        tuple: (citations, snippets) where citations is a list of dicts with title/url,
               and snippets is a list of content strings
    """
    if not claim or not claim.strip():
        return [], []

    tavily = _get_tavily_client()
    if tavily is None:
        logger.error("Tavily client not available")
        return [], []

    try:
        # Use advanced search for better results
        response = tavily.search(
            query=claim,
            search_depth="advanced",  # Changed to advanced for better results
            max_results=10,  # Increased for better coverage
            include_answer=True,  # Get direct answers if available
            include_raw_content=True  # Get more content
        )
    except Exception as e:
        logger.error(f"Tavily search failed for claim '{claim[:50]}...': {e}")
        return [], []

    citations = []
    snippets = []

    try:
        results = response.get("results", [])
        for result in results:
            title = result.get("title", "")
            url = result.get("url", "")
            content = result.get("content", "")

            if url:  # Only add if URL exists
                citations.append({
                    "title": title or "Untitled",
                    "url": url
                })

            if content:
                snippets.append(content)
    except Exception as e:
        logger.error(f"Error processing search results: {e}")
        return citations, snippets

    return citations, snippets


def search_web_for_claim(claim: str, domain: str = "general") -> tuple[list[dict], list[str]]:
    """
    Search the web for a claim with intelligent caching.
    Uses semantic similarity to reuse similar searches.
    """
    return get_cached_or_search(claim, domain, _perform_tavily_search)

