"""
FastAPI API Package
"""

from fastapi import APIRouter

# Import the main router from routes
from src.api.routes import router

__all__ = ["router"]