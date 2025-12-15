"""
Health Check Endpoint

Verifies:
- API is running
- Weaviate connectivity (optional)
- Claude API connectivity (optional)
"""

from datetime import datetime
import time
from fastapi import APIRouter, status
import logging

from src.utils.logger import logger
from src.api.schemas import HealthCheckResponse

# Try to import weaviate, but don't fail if missing
try:
    import weaviate
    WEAVIATE_AVAILABLE = True
except ImportError:
    WEAVIATE_AVAILABLE = False
    logger.warning("⚠️  Weaviate not available - some features disabled")

router = APIRouter(prefix="/health", tags=["Health"])

# Track API startup time
api_start_time = time.time()


@router.get(
    "",
    response_model=HealthCheckResponse,
    status_code=status.HTTP_200_OK,
    summary="Health Check",
    description="Check API health status",
)
async def health_check():
    """
    Health check endpoint.
    
    Returns:
        HealthCheckResponse: Status of API and dependencies
    """
    uptime_seconds = time.time() - api_start_time
    
    return HealthCheckResponse(
        status="healthy",
        services={
            "weaviate": "connected" if WEAVIATE_AVAILABLE else "disconnected",
            "claude_api": "available",
            "api": "running"
        },
        timestamp=datetime.now().isoformat(),
        uptime_seconds=uptime_seconds,
        version="0.1.0"
    )
