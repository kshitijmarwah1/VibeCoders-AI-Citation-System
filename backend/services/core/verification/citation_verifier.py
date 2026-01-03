"""
Citation verification module.
Verifies if citations (URLs, DOIs) are valid and accessible.
"""
import requests
import logging
from typing import Dict, List, Tuple
from urllib.parse import urlparse
import asyncio
import aiohttp

logger = logging.getLogger(__name__)

async def verify_url_async(session: aiohttp.ClientSession, url: str, timeout: int = 5) -> Tuple[str, bool, str]:
    """
    Asynchronously verify if a URL is accessible.
    Returns: (url, is_valid, error_message)
    """
    try:
        async with session.get(url, timeout=aiohttp.ClientTimeout(total=timeout), allow_redirects=True) as response:
            is_valid = response.status < 400
            error_msg = "" if is_valid else f"HTTP {response.status}"
            return (url, is_valid, error_msg)
    except asyncio.TimeoutError:
        return (url, False, "Timeout")
    except Exception as e:
        logger.warning(f"URL verification failed for {url}: {e}")
        return (url, False, str(e))


async def verify_citations_async(citations: List[Dict]) -> Dict[str, any]:
    """
    Verify multiple citations asynchronously.
    Returns verification status for each citation.
    """
    if not citations:
        return {"verified": [], "invalid": [], "total": 0}
    
    verified = []
    invalid = []
    
    async with aiohttp.ClientSession() as session:
        tasks = []
        for citation in citations:
            url = citation.get("url", "")
            if url:
                tasks.append(verify_url_async(session, url))
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        for i, result in enumerate(results):
            if isinstance(result, Exception):
                invalid.append({
                    "url": citations[i].get("url", ""),
                    "title": citations[i].get("title", ""),
                    "error": str(result)
                })
            else:
                url, is_valid, error_msg = result
                citation_data = {
                    "url": url,
                    "title": citations[i].get("title", ""),
                }
                if is_valid:
                    verified.append(citation_data)
                else:
                    citation_data["error"] = error_msg
                    invalid.append(citation_data)
    
    return {
        "verified": verified,
        "invalid": invalid,
        "total": len(citations),
        "verification_rate": len(verified) / len(citations) if citations else 0
    }


def verify_citations_sync(citations: List[Dict]) -> Dict[str, any]:
    """
    Synchronous citation verification (fallback).
    """
    if not citations:
        return {"verified": [], "invalid": [], "total": 0}
    
    verified = []
    invalid = []
    
    for citation in citations:
        url = citation.get("url", "")
        if not url:
            continue
        
        try:
            response = requests.head(url, timeout=5, allow_redirects=True)
            if response.status_code < 400:
                verified.append({
                    "url": url,
                    "title": citation.get("title", "")
                })
            else:
                invalid.append({
                    "url": url,
                    "title": citation.get("title", ""),
                    "error": f"HTTP {response.status_code}"
                })
        except Exception as e:
            logger.warning(f"Citation verification failed for {url}: {e}")
            invalid.append({
                "url": url,
                "title": citation.get("title", ""),
                "error": str(e)
            })
    
    return {
        "verified": verified,
        "invalid": invalid,
        "total": len(citations),
        "verification_rate": len(verified) / len(citations) if citations else 0
    }

