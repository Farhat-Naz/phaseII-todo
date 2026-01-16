"""
Vercel Serverless Function for Backend API
"""
# Import the FastAPI app directly from the api/app folder
from app.main import app

# Export the app for Vercel
# Vercel automatically detects and wraps FastAPI apps
