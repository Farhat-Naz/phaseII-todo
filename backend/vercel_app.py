"""
Vercel serverless function entry point for FastAPI backend.
Simplified version that avoids import-time database connections.
"""
import sys
import os

# Add the backend directory to Python path
sys.path.insert(0, os.path.dirname(__file__))

try:
    from app.main import app
    handler = app
except Exception as e:
    # If main app fails, create a minimal fallback app
    from fastapi import FastAPI
    from fastapi.middleware.cors import CORSMiddleware

    app = FastAPI(title="Todo API (Fallback)")

    # Add CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/")
    async def root():
        return {
            "status": "error",
            "message": f"Failed to initialize app: {str(e)}",
            "error_type": type(e).__name__
        }

    @app.get("/health")
    async def health():
        return {
            "status": "unhealthy",
            "error": str(e)
        }

    handler = app

# For local testing
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
