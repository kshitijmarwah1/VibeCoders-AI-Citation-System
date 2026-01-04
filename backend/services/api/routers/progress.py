"""
Progress tracking endpoint using Server-Sent Events (SSE).
"""
from fastapi import APIRouter
from fastapi.responses import StreamingResponse
import asyncio
import json
import logging

logger = logging.getLogger(__name__)

try:
    from sse_starlette.sse import EventSourceResponse
    SSE_AVAILABLE = True
except ImportError:
    SSE_AVAILABLE = False
    logger.warning("sse-starlette not available, using fallback")
router = APIRouter(prefix="/progress", tags=["Progress"])

# In-memory progress store (in production, use Redis or similar)
_progress_store = {}

def update_progress(task_id: str, completed: int, total: int, current: str, status: str = "processing"):
    """Update progress for a task."""
    _progress_store[task_id] = {
        "completed": completed,
        "total": total,
        "current": current,
        "status": status,
        "percentage": (completed / total * 100) if total > 0 else 0
    }

def get_progress(task_id: str):
    """Get current progress for a task."""
    return _progress_store.get(task_id, {
        "completed": 0,
        "total": 0,
        "current": "",
        "status": "pending",
        "percentage": 0
    })

async def progress_stream(task_id: str):
    """Stream progress updates via SSE."""
    while True:
        progress = get_progress(task_id)
        
        # Send progress update
        data = json.dumps(progress)
        yield {
            "event": "progress",
            "data": data
        }
        
        # If completed, send final event and break
        if progress["status"] in ["completed", "error"]:
            yield {
                "event": "done",
                "data": data
            }
            break
        
        await asyncio.sleep(0.5)  # Update every 500ms

@router.get("/stream/{task_id}")
async def stream_progress(task_id: str):
    """Stream progress updates for a task."""
    if SSE_AVAILABLE:
        return EventSourceResponse(progress_stream(task_id))
    else:
        # Fallback: return JSON polling endpoint
        async def generate():
            while True:
                progress = get_progress(task_id)
                yield f"data: {json.dumps(progress)}\n\n"
                if progress["status"] in ["completed", "error"]:
                    break
                await asyncio.sleep(0.5)
        
        return StreamingResponse(
            generate(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

@router.get("/{task_id}")
async def get_progress_status(task_id: str):
    """Get current progress status."""
    progress = get_progress(task_id)
    # If task doesn't exist yet, return pending status instead of 404
    if progress["status"] == "pending" and progress["percentage"] == 0:
        # Task might not be initialized yet, return a default pending response
        return {
            "completed": 0,
            "total": 0,
            "current": "Initializing...",
            "status": "pending",
            "percentage": 0
        }
    return progress

