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
    Verify multiple claims in parallel batches with real progress tracking.
    
    Args:
        claims: List of claim strings
        domain: Domain for verification
        batch_size: Number of claims to process in parallel
        progress_callback: Callback function(completed, total, current_claim)
    
    Returns:
        List of verification results
    """
    results = []
    total = len(claims)
    
    # Process in batches to avoid overwhelming the system
    for i in range(0, total, batch_size):
        batch = claims[i:i + batch_size]
        batch_num = (i // batch_size) + 1
        total_batches = (total + batch_size - 1) // batch_size
        
        logger.info(f"Processing batch {batch_num}/{total_batches} ({len(batch)} claims)")
        
        # Process batch in parallel with individual progress tracking
        async def verify_with_progress(claim: str, index: int):
            """Verify a single claim and update progress."""
            try:
                # Update progress before starting
                if progress_callback:
                    progress_callback(i + index, total, f"Searching for: {claim[:50]}...")
                
                result = await verify_claim_async(claim, domain)
                
                # Update progress after completion
                if progress_callback:
                    progress_callback(i + index + 1, total, f"Completed: {claim[:50]}...")
                
                return result
            except Exception as e:
                logger.error(f"Verification failed for claim {i+index+1}: {e}")
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
        
        # Create tasks with progress tracking
        batch_tasks = [verify_with_progress(claim, j) for j, claim in enumerate(batch)]
        batch_results = await asyncio.gather(*batch_tasks, return_exceptions=True)
        
        # Handle results
        for result in batch_results:
            if isinstance(result, Exception):
                logger.error(f"Unexpected error in batch: {result}")
                continue
            results.append(result)
        
        # Small delay between batches to prevent rate limiting
        if i + batch_size < total:
            await asyncio.sleep(0.1)
    
    return results

