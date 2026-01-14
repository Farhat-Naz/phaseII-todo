"""
Vercel serverless function entry point for FastAPI backend.

This file adapts the FastAPI app for Vercel's serverless environment.
Disables lifespan events for serverless compatibility.
"""
from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os
import logging

from app.routers import auth, todos

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Create FastAPI application WITHOUT lifespan for Vercel
app = FastAPI(
    title="Todo API",
    version="1.0.0",
    description="Secure REST API for todo management with JWT authentication",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ============================================
# CORS Configuration
# ============================================

# Allow all origins for simplicity (already configured in main.py)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

logger.info("CORS enabled for ALL origins")

# ============================================
# Exception Handlers
# ============================================

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(
    request: Request,
    exc: RequestValidationError
) -> JSONResponse:
    """Handle Pydantic validation errors."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": " -> ".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    logger.warning(f"Validation error on {request.url.path}: {errors}")

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "detail": "Validation error",
            "errors": errors
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(
    request: Request,
    exc: Exception
) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(f"Unexpected error on {request.url.path}: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "Internal server error",
            "message": str(exc) if os.getenv("DEBUG", "False") == "True" else "An unexpected error occurred"
        }
    )

# ============================================
# Health Check
# ============================================

@app.get("/", tags=["Health"])
async def root():
    """Root endpoint - health check."""
    return {
        "status": "ok",
        "message": "Todo API is running",
        "version": "1.0.0",
        "docs": "/docs"
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint for monitoring."""
    return {
        "status": "healthy",
        "service": "todo-api",
        "version": "1.0.0"
    }

# ============================================
# API Routers
# ============================================

app.include_router(auth.router, tags=["Authentication"])
app.include_router(todos.router, tags=["Todos"])

# Vercel requires a handler function
handler = app

# For local testing compatibility
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
