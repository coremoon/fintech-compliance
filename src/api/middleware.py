"""
FastAPI Middleware Configuration
"""

from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import logging

logger = logging.getLogger(__name__)


def setup_middleware(app: FastAPI) -> None:
    """Setup all middleware"""
    
    logger.info("Setting up middleware...")
    
    # Add CORS middleware ONLY - no LoggingMiddleware!
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:3000",
            "http://localhost:8088",
            "http://127.0.0.1:3000",
            "http://127.0.0.1:8088",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    logger.info("CORS configured")
    logger.info("Middleware setup complete")


def register_exception_handlers(app: FastAPI) -> None:
    """Register global exception handlers"""
    
    logger.info("Registering exception handlers...")
    
    @app.exception_handler(Exception)
    async def general_exception_handler(request, exc: Exception):
        """Handle all exceptions"""
        logger.error(f"Unexpected error: {str(exc)}", exc_info=True)
        
        return JSONResponse(
            status_code=500,
            content={
                "status": "error",
                "error_code": "INTERNAL_ERROR",
                "message": "An unexpected error occurred",
                "details": None,
            },
        )
    
    logger.info("Exception handlers registered")
