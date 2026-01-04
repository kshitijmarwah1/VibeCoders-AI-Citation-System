from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel, HttpUrl
import tempfile
import shutil
import os
import logging
import uuid
import asyncio

from services.core.claims.domain_detector import detect_domain
from services.core.claims.extractor import extract_claims
from services.core.verification.verify_async import verify_claims_batch, verify_claim_async
from services.core.verification.citation_verifier import verify_citations_async
from services.core.scoring.aggregation import calculate_overall_score
from services.core.explainability.traces import extract_citations
from services.core.input.normalize import normalize_input
from services.api.routers.progress import update_progress

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/verify", tags=["Verification"])


class TextInput(BaseModel):
    text: str


class UrlInput(BaseModel):
    url: HttpUrl | str


class BatchInput(BaseModel):
    text: str | None = None
    urls: list[HttpUrl | str] | None = None


@router.post("/text/async")
async def verify_text_async(data: TextInput):
    """Verify text input asynchronously, returns task_id for progress tracking."""
    try:
        task_id = str(uuid.uuid4())
        normalized_text = data.text
        
        # Start verification in background
        asyncio.create_task(run_verification_async(normalized_text, task_id, "text"))
        
        return {"task_id": task_id, "status": "started"}
    except Exception as e:
        logger.error(f"Async text verification failed: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid text input: {str(e)}")


async def run_verification_async(normalized_text: str, task_id: str = None, input_type: str = "general"):
    """
    Run the complete verification pipeline asynchronously with REAL progress tracking.
    
    Args:
        normalized_text: The text to verify
        task_id: Task ID for progress tracking
        input_type: Type of input ("text", "url", "file", "general")
    """
    if not normalized_text or not normalized_text.strip():
        raise HTTPException(status_code=400, detail="No text content provided")

    try:
        is_text_input = input_type == "text"
        
        # Step 1: Extract claims with granular progress for text inputs
        if task_id:
            if is_text_input:
                update_progress(task_id, 2, 100, "Analyzing text structure...", "processing")
                await asyncio.sleep(0.1)  # Small delay to show progress
                update_progress(task_id, 4, 100, "Segmenting sentences...", "processing")
                await asyncio.sleep(0.1)
            update_progress(task_id, 5, 100, "Extracting claims from text...", "processing")
        
        claims = extract_claims(normalized_text)
        
        # Additional progress for text inputs after extraction
        if is_text_input and task_id and claims:
            await asyncio.sleep(0.1)
            update_progress(task_id, 7, 100, f"Found {len(claims)} claim(s) to verify...", "processing")
        
        if not claims:
            extracted_citations = extract_citations(normalized_text)
            if task_id:
                update_progress(task_id, 100, 100, "No claims found", "completed")
            return {
                "domain": "general",
                "total_claims": 0,
                "overall_reliability": 0.0,
                "claims": [],
                "extracted_citations": extracted_citations,
                "citation_verification": {"verified": [], "invalid": [], "total": 0}
            }

        # Step 2: Detect domain (7-10% for text, 5-10% for others)
        if task_id:
            if is_text_input:
                await asyncio.sleep(0.1)
            update_progress(task_id, 10, 100, "Detecting domain...", "processing")
        
        domain = detect_domain(normalized_text)
        
        # Step 3: Verify claims in parallel batches (10-85% of progress)
        # Progress is tracked by batch completion
        # For text inputs with few claims, use claim-level progress instead
        if is_text_input and len(claims) <= 3:
            # For very short text inputs, track individual claim progress
            def progress_callback_text(completed: int, total: int, current: str):
                if task_id:
                    # Real progress: 10% to 85% based on claim completion
                    base_percentage = 10
                    progress_range = 75  # 85 - 10
                    percentage = base_percentage + int((completed / total) * progress_range)
                    update_progress(task_id, percentage, 100, current, "processing")
            
            # Process claims individually for better progress visibility
            results = []
            for idx, claim in enumerate(claims):
                if task_id:
                    progress_callback_text(idx, len(claims), f"Verifying claim {idx + 1}/{len(claims)}...")
                result = await verify_claim_async(claim, domain)
                results.append(result)
                if task_id:
                    progress_callback_text(idx + 1, len(claims), f"Completed claim {idx + 1}/{len(claims)}")
        else:
            # Batch processing for longer inputs
            def progress_callback(completed_batches: int, total_batches: int, current: str):
                if task_id:
                    # Real progress: 10% to 85% based on batch completion
                    base_percentage = 10
                    progress_range = 75  # 85 - 10
                    percentage = base_percentage + int((completed_batches / total_batches) * progress_range)
                    update_progress(task_id, percentage, 100, current, "processing")
            
            results = await verify_claims_batch(
                claims,
                domain,
                batch_size=5,
                progress_callback=progress_callback
            )

        # Step 4: Verify citations (85-95% of progress)
        if task_id:
            update_progress(task_id, 85, 100, "Verifying citations...", "processing")
        
        all_citations = []
        for result in results:
            all_citations.extend(result.get("citations", []))
        
        citation_verification = await verify_citations_async(all_citations) if all_citations else {"verified": [], "invalid": [], "total": 0}
        
        # Step 5: Calculate overall score and finalize (95-100% of progress)
        if task_id:
            update_progress(task_id, 95, 100, "Calculating final scores...", "processing")
        
        overall_score = calculate_overall_score(results)
        extracted_citations = extract_citations(normalized_text)

        if task_id:
            update_progress(task_id, 100, 100, "Verification complete", "completed")

        return {
            "domain": domain,
            "total_claims": len(results),
            "overall_reliability": overall_score,
            "claims": results,
            "extracted_citations": extracted_citations,
            "citation_verification": citation_verification
        }
    except Exception as e:
        logger.error(f"Verification pipeline failed: {e}")
        if task_id:
            update_progress(task_id, 0, 100, f"Error: {str(e)}", "error")
        raise HTTPException(status_code=500, detail=f"Verification failed: {str(e)}")


def run_verification(normalized_text: str):
    """
    Synchronous wrapper for backward compatibility.
    """
    return asyncio.run(run_verification_async(normalized_text))


@router.post("/text")
async def verify_text(data: TextInput):
    """Verify text input with progress tracking."""
    try:
        if not data.text or not data.text.strip():
            raise HTTPException(status_code=400, detail="Text input cannot be empty")
        
        # Generate task_id and return it in response header for progress tracking
        task_id = str(uuid.uuid4())
        normalized_text = data.text.strip()
        
        logger.info(f"Starting text verification for {len(normalized_text)} characters, task_id: {task_id}")
        
        # Run verification with progress tracking
        result = await run_verification_async(normalized_text, task_id, "text")
        
        logger.info(f"Text verification completed: {result.get('total_claims', 0)} claims found")
        
        # Return result with task_id in response
        result["task_id"] = task_id
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Text verification failed: {e}", exc_info=True)
        raise HTTPException(status_code=400, detail=f"Invalid text input: {str(e)}")


@router.post("/url")
async def verify_url(data: UrlInput):
    """Verify content from URL."""
    try:
        task_id = str(uuid.uuid4())
        url = str(data.url)
        normalized_text = normalize_input(urls=[url])
        result = await run_verification_async(normalized_text, task_id, "url")
        result["task_id"] = task_id
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"URL verification failed: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to process URL: {str(e)}")


@router.post("/file")
async def verify_file(file: UploadFile = File(...)):
    """Verify content from uploaded file (PDF or DOCX)."""
    tmp_path = None
    try:
        task_id = str(uuid.uuid4())
        
        # Validate file type
        if not file.filename:
            raise HTTPException(status_code=400, detail="No filename provided")
        
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in [".pdf", ".docx", ".doc"]:
            raise HTTPException(status_code=400, detail=f"Unsupported file type: {file_ext}. Supported: .pdf, .docx, .doc")

        # Save uploaded file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=file_ext) as tmp:
            shutil.copyfileobj(file.file, tmp)
            tmp_path = tmp.name

        update_progress(task_id, 5, 100, "Extracting text from file...", "processing")
        normalized_text = normalize_input(files=[tmp_path])
        result = await run_verification_async(normalized_text, task_id, "file")
        result["task_id"] = task_id
        return result
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"File verification failed: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to process file: {str(e)}")
    finally:
        # Cleanup temp file
        if tmp_path and os.path.exists(tmp_path):
            try:
                os.unlink(tmp_path)
            except Exception as e:
                logger.warning(f"Failed to delete temp file {tmp_path}: {e}")


@router.post("/batch")
async def verify_batch(data: BatchInput):
    """Verify batch input (text and/or URLs)."""
    try:
        task_id = str(uuid.uuid4())
        if not data.text and not data.urls:
            raise HTTPException(status_code=400, detail="At least one of 'text' or 'urls' must be provided")
        
        urls = [str(url) for url in data.urls] if data.urls else None
        normalized_text = normalize_input(text=data.text, urls=urls)
        input_type = "text" if data.text and not urls else "general"
        return await run_verification_async(normalized_text, task_id, input_type)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Batch verification failed: {e}")
        raise HTTPException(status_code=400, detail=f"Failed to process batch input: {str(e)}")