from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from services.api.routers.verify import router as verify_router
from services.api.routers.progress import router as progress_router
import os

app = FastAPI(
    title="AI Verification Service",
    description="Universal AI Hallucination & Citation Verification System",
    version="1.0.0"
)

# CORS - Allow all origins in development, restrict in production
cors_origins = os.getenv("CORS_ORIGINS", "http://localhost:3000").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(verify_router)
app.include_router(progress_router)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "AI Verification Service"}


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )
