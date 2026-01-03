import requests
from bs4 import BeautifulSoup
import logging

logger = logging.getLogger(__name__)

def extract_text_from_url(url: str) -> str:
    """
    Extract text from URL with proper error handling and headers.
    """
    if not url or not url.startswith(("http://", "https://")):
        raise ValueError(f"Invalid URL format: {url}")

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }

    try:
        response = requests.get(url, timeout=15, headers=headers, allow_redirects=True)
        response.raise_for_status()
        
        # Check content type
        content_type = response.headers.get("content-type", "").lower()
        if "text/html" not in content_type:
            logger.warning(f"URL {url} does not return HTML content")
            return ""

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove scripts, styles, and other non-content elements
        for tag in soup(["script", "style", "noscript", "meta", "link", "head"]):
            tag.decompose()

        # Try to extract main content
        main_content = soup.find("main") or soup.find("article") or soup.find("body")
        if main_content:
            text = main_content.get_text(separator="\n")
        else:
            text = soup.get_text(separator="\n")

        lines = [line.strip() for line in text.splitlines() if line.strip()]

        if not lines:
            raise ValueError(f"No text content found in URL: {url}")

        return "\n".join(lines)
    except requests.exceptions.Timeout:
        logger.error(f"Timeout while fetching URL: {url}")
        raise ValueError(f"Request timeout for URL: {url}")
    except requests.exceptions.RequestException as e:
        logger.error(f"Failed to fetch URL {url}: {e}")
        raise ValueError(f"Failed to fetch URL: {url}")
    except Exception as e:
        logger.error(f"Error extracting text from URL {url}: {e}")
        raise ValueError(f"Failed to extract text from URL: {url}")
