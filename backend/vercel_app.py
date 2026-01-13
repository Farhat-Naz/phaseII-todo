"""
Vercel serverless function entry point for FastAPI backend.

This file adapts the FastAPI app for Vercel's serverless environment.
"""
from app.main import app

# Vercel requires a handler function
handler = app

# For local testing compatibility
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
