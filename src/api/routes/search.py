"""
Search Endpoints - Search regulations using Weaviate (optional).
"""

from fastapi import APIRouter, status, HTTPException
import logging

from src.api.schemas import RegulationSearchRequest, RegulationSearchResponse

try:
    import weaviate
    WEAVIATE_AVAILABLE = True
except ImportError:
    WEAVIATE_AVAILABLE = False

router = APIRouter(prefix="/regulations", tags=["Search"])


@router.post("/search", response_model=RegulationSearchResponse, status_code=status.HTTP_200_OK)
async def search_regulations(request: RegulationSearchRequest) -> RegulationSearchResponse:
    """Search regulations endpoint."""
    
    if not WEAVIATE_AVAILABLE:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Weaviate vector database not available"
        )
    
    return RegulationSearchResponse(
        query=request.query,
        results=[],
        total_results=0,
        search_time_ms=0
    )
