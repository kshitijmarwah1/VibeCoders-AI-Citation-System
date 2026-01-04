from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException
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


@app.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "service": "AI Verification Service",
        "version": "1.0.0",
        "description": "Universal AI Hallucination & Citation Verification System",
        "status": "running",
        "endpoints": {
            "docs": "/docs",
            "redoc": "/redoc",
            "health": "/health",
            "verify_text": "/verify/text",
            "verify_url": "/verify/url",
            "verify_file": "/verify/file",
            "verify_batch": "/verify/batch",
            "progress": "/progress/{task_id}",
            "progress_stream": "/progress/stream/{task_id}"
        }
    }


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


@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """Handle HTTP exceptions (404, etc.) with better error messages."""
    if exc.status_code == 404:
        return JSONResponse(
            status_code=404,
            content={
                "detail": "Endpoint not found",
                "message": f"The requested endpoint '{request.url.path}' does not exist.",
                "available_endpoints": {
                    "root": "/",
                    "docs": "/docs",
                    "redoc": "/redoc",
                    "health": "/health",
                    "verify_text": "POST /verify/text",
                    "verify_url": "POST /verify/url",
                    "verify_file": "POST /verify/file",
                    "verify_batch": "POST /verify/batch",
                    "progress": "GET /progress/{task_id}",
                    "progress_stream": "GET /progress/stream/{task_id}"
                }
            }
        )
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handle request validation errors."""
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors(), "body": exc.body}
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global exception handler for unhandled errors."""
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error", "error": str(exc)}
    )
