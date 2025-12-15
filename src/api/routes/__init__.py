from fastapi import APIRouter

router = APIRouter(prefix="/api/v1")

# Super simple health endpoint - no imports, no logic
@router.get("/health")
async def health():
    """Health check - always returns OK"""
    try:
        return {
            "status": "healthy",
            "service": "fintech-compliance-api",
            "version": "0.1.0"
        }
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }

__all__ = ["router"]