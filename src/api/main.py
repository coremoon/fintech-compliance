"""
FastAPI Application Entry Point

Main application server for the Blockchain Compliance Advisory API.

Port: 8088
Docs: http://localhost:8088/docs
"""

from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import uvicorn
import logging

from src.utils.logger import logger
from src.api import config
from src.api.middleware import setup_middleware, register_exception_handlers
from src.api.routes import router

# ============================================================================
# LIFESPAN CONTEXT MANAGER (Modern FastAPI 0.93+)
# ============================================================================

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown event handler using modern lifespan context manager.
    Replaces deprecated @app.on_event("startup") and @app.on_event("shutdown")
    """
    
    # STARTUP
    logger.info("=" * 80)
    logger.info(config.CONFIG_SUMMARY)
    logger.info("=" * 80)
    
    try:
        config.validate_config()
        logger.info("✅ Configuration validated")
    except Exception as e:
        logger.error(f"❌ Configuration validation failed: {str(e)}")
        raise
    
    yield  # Application runs here
    
    # SHUTDOWN
    logger.info("API server shutting down")


# ============================================================================
# CREATE FASTAPI APP
# ============================================================================

app = FastAPI(
    title=config.API_TITLE,
    description=config.API_DESCRIPTION,
    version=config.API_VERSION,
    docs_url="/docs",
    openapi_url="/openapi.json",
    redoc_url="/redoc",
    lifespan=lifespan
)

# ============================================================================
# SETUP MIDDLEWARE & EXCEPTION HANDLERS
# ============================================================================

try:
    logger.info("Setting up middleware...")
    setup_middleware(app)
    logger.info("Registering exception handlers...")
    register_exception_handlers(app)
except Exception as e:
    logger.error(f"Failed to setup middleware: {str(e)}", exc_info=True)
    raise

# ============================================================================
# INCLUDE ROUTES
# ============================================================================

app.include_router(router)

# ============================================================================
# ROOT ENDPOINT
# ============================================================================

@app.get("/", summary="API Root", description="Blockchain Compliance Advisory API")
async def root():
    return JSONResponse({
        "title": config.API_TITLE,
        "version": config.API_VERSION,
        "documentation": "http://localhost:8088/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "analyze_project": "/api/v1/analyze/project",
            "analyze_contract": "/api/v1/analyze/contract",
            "search_regulations": "/api/v1/search/regulations",
            "enforcement_cases": "/api/v1/search/enforcement-cases"
        }
    })


# ============================================================================
# MAIN ENTRY POINT
# ============================================================================

def main():
    """Start the API server."""
    logger.info(f"Starting API server on {config.API_HOST}:{config.API_PORT}")
    logger.info(f"Documentation: http://localhost:{config.API_PORT}/docs")
    
    uvicorn.run(
        "src.api.main:app",
        host=config.API_HOST,
        port=config.API_PORT,
        workers=config.API_WORKERS,
        reload=config.API_RELOAD,
        log_level=config.LOG_LEVEL.lower()
    )


if __name__ == "__main__":
    main()
