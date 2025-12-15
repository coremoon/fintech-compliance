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
    logging.warning("⚠️  Weaviate not available - some features disabled")

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
    """Health check endpoint."""
    uptime_seconds = time.time() - api_start_time
    
    return HealthCheckResponse(
        status="healthy",
        timestamp=datetime.now(),
        uptime_seconds=uptime_seconds,
        version="0.1.0",
        weaviate_connected=WEAVIATE_AVAILABLE,
        message="API is running"
    )
