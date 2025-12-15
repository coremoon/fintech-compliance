"""
FastAPI Routes Package

Routes for:
- Health checks
- Regulation search (optional - requires Weaviate)
- Project analysis (optional)
- Contract analysis (optional)
"""

from fastapi import APIRouter
import logging

logger = logging.getLogger(__name__)

# Create main router
router = APIRouter(prefix="/api/v1")

# Always load health routes
try:
    from . import health
    router.include_router(health.router)
    logger.info("✅ Health routes loaded")
except Exception as e:
    logger.error(f"❌ Health routes failed: {e}")
    raise

# Optionally load search routes (requires Weaviate)
try:
    from . import search
    router.include_router(search.router)
    logger.info("✅ Search routes loaded")
except Exception as e:
    logger.warning(f"⚠️  Search routes skipped: {e}")

# Optionally load analyze routes
try:
    from . import analyze
    router.include_router(analyze.router)
    logger.info("✅ Analyze routes loaded")
except Exception as e:
    logger.warning(f"⚠️  Analyze routes skipped: {e}")

__all__ = ["router"]
