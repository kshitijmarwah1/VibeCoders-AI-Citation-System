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

# CORS Configuration - MUST be configured before adding routers
cors_origins_env = os.getenv("CORS_ORIGINS", "")
cors_origins = cors_origins_env.split(",") if cors_origins_env else []

# Default allowed origins
default_origins = [
    "https://vibe-coders-ai-citation-system.vercel.app",  # Production frontend (Vercel)
    "http://localhost:3000",  # Local development
    "http://localhost:3001",  # Alternative local port
]

# Combine environment origins with defaults, removing duplicates and empty strings
all_origins = list(set(
    [origin.strip() for origin in cors_origins if origin.strip()] + 
    default_origins
))

# Print allowed origins for debugging (remove in production if sensitive)
print(f"CORS allowed origins: {all_origins}")

# Add CORS middleware - CRITICAL: Must be added BEFORE routers
app.add_middleware(
    CORSMiddleware,
    allow_origins=all_origins,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS", "HEAD", "PATCH"],
    allow_headers=["*"],
    expose_headers=["*"],
    max_age=3600,
)

app.include_router(verify_router)
app.include_router(progress_router)


@app.get("/health")
def health():
    """Health check endpoint."""
    return {"status": "ok", "service": "AI Verification Service"}


@app.get("/cors-test")
def cors_test():
    """Test endpoint to verify CORS is working."""
    return {
        "status": "ok",
        "message": "CORS is configured correctly",
        "allowed_origins": all_origins
    }


@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )
