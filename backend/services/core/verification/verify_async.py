"""
Async version of claim verification for better performance.
Supports batching and parallel processing.
"""
import asyncio
import logging
from typing import List, Dict, Callable
from services.core.verification.verify import verify_claim

logger = logging.getLogger(__name__)

async def verify_claim_async(claim: str, domain: str = "general") -> Dict:
    """
    Async wrapper for verify_claim.
    Runs verification in thread pool to avoid blocking.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, verify_claim, claim, domain)


async def verify_claims_batch(
    claims: List[str],
    domain: str = "general",
    batch_size: int = 5,
    progress_callback: Callable[[int, int, str], None] = None
) -> List[Dict]:
    """
    Verify multiple claims in parallel batches with batch-level progress tracking.
    
    Args:
        claims: List of claim strings
        domain: Domain for verification
        batch_size: Number of claims to process in parallel
        progress_callback: Callback function(completed_batches, total_batches, message)
    
    Returns:
        List of verification results
    """
    results = []
    total = len(claims)
    total_batches = (total + batch_size - 1) // batch_size
    
    # Process in batches to avoid overwhelming the system
    for i in range(0, total, batch_size):
        batch = claims[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        
        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} claims)")
        
        # Update progress at batch start
        if progress_callback:
            progress_callback(
                batch_num - 1,  # completed batches (0-indexed for start)
                total_batches,
                f"Processing batch {batch_num}/{total_batches} ({len(batch)} claims)..."
            )
        
        # Process batch in parallel without individual claim progress tracking
        async def verify_claim_simple(claim: str):
            """Verify a single claim without progress tracking."""
            try:
                result = await verify_claim_async(claim, domain)
                return result
            except Exception as e:
                logger.error(f"Verification failed for claim: {e}")
                return {
                    "claim": claim,
                    "status": "error",
                    "confidence": 0.0,
                    "similarity": 0.0,
                    "credibility": 0.0,
                    "contradicted": False,
                    "citations": [],
                    "explanation": f"Verification failed: {str(e)}"
                }
        
        # Create tasks for batch processing
        batch_tasks = [verify_claim_simple(claim) for claim in batch]
        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
        
        # Handle results
        for result in batch_results:
            if isinstance(result, Exception):
                logger.error(f"Unexpected error in batch: {result}")
                continue
            results.append(result)
        
        # Update progress after batch completion
        if progress_callback:
            progress_callback(
                batch_num,  # completed batches (1-indexed for completion)
                total_batches,
                f"Completed batch {batch_num}/{total_batches} ({len(batch)} claims verified)"
            )
        
        # Small delay between batches to prevent rate limiting
        if i + batch_size < total:
            await asyncio.sleep(0.1)
    
    return results

