"""
FastAPI Configuration

Central configuration for API server, Weaviate connection,
Claude API settings, and rate limiting.
"""

import os
from typing import Optional

# ============================================================================
# SERVER CONFIGURATION
# ============================================================================

API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", "8088"))
API_WORKERS = int(os.getenv("API_WORKERS", "4"))
API_RELOAD = os.getenv("API_RELOAD", "false").lower() == "true"

# ============================================================================
# WEAVIATE CONFIGURATION
# ============================================================================

WEAVIATE_HOST = os.getenv("WEAVIATE_HOST", "localhost")
WEAVIATE_PORT = int(os.getenv("WEAVIATE_PORT", "8098"))
WEAVIATE_URL = f"http://{WEAVIATE_HOST}:{WEAVIATE_PORT}"
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "W3aviate")

# Health check timeout (seconds)
WEAVIATE_TIMEOUT = (10, 120)  # (connection, request)

# ============================================================================
# CLAUDE API CONFIGURATION
# ============================================================================

CLAUDE_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5-20250929")
CLAUDE_MAX_TOKENS = int(os.getenv("CLAUDE_MAX_TOKENS", "4096"))

# ============================================================================
# RATE LIMITING
# ============================================================================

# Rate limiting: requests per minute per endpoint
RATE_LIMIT_ANALYZE_PROJECT = int(os.getenv("RATE_LIMIT_ANALYZE_PROJECT", "10"))
RATE_LIMIT_ANALYZE_CONTRACT = int(os.getenv("RATE_LIMIT_ANALYZE_CONTRACT", "20"))
RATE_LIMIT_SEARCH = int(os.getenv("RATE_LIMIT_SEARCH", "30"))
RATE_LIMIT_GENERAL = int(os.getenv("RATE_LIMIT_GENERAL", "100"))

# ============================================================================
# API METADATA
# ============================================================================

API_TITLE = "Blockchain Compliance Advisory API"
API_DESCRIPTION = """
AI-powered compliance analysis system for blockchain/crypto projects.

Provides:
- Regulatory compliance analysis
- Smart contract analysis (Simplicity-HL)
- Enforcement case research
- Risk assessment reports
"""
API_VERSION = "1.0.0"

# ============================================================================
# CORS CONFIGURATION
# ============================================================================

CORS_ORIGINS = [
    "http://localhost:3000",      # Frontend development
    "http://localhost:8088",      # API itself
    "http://127.0.0.1:3000",
    "http://127.0.0.1:8088",
]

CORS_ALLOW_CREDENTIALS = True
CORS_ALLOW_METHODS = ["GET", "POST", "OPTIONS"]
CORS_ALLOW_HEADERS = ["Content-Type", "Authorization"]

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# ============================================================================
# FEATURE FLAGS
# ============================================================================

FEATURE_CONTRACT_ANALYSIS = os.getenv("FEATURE_CONTRACT_ANALYSIS", "true").lower() == "true"
FEATURE_PROJECT_ANALYSIS = os.getenv("FEATURE_PROJECT_ANALYSIS", "true").lower() == "true"
FEATURE_SEARCH = os.getenv("FEATURE_SEARCH", "true").lower() == "true"
FEATURE_ENFORCEMENT_CASES = os.getenv("FEATURE_ENFORCEMENT_CASES", "true").lower() == "true"

# ============================================================================
# VALIDATION
# ============================================================================

def validate_config() -> bool:
    """Validate critical configuration settings."""
    
    if not CLAUDE_API_KEY:
        raise ValueError("ANTHROPIC_API_KEY environment variable not set!")
    
    if not WEAVIATE_URL:
        raise ValueError("WEAVIATE_URL not configured!")
    
    return True

# ============================================================================
# SUMMARY
# ============================================================================

CONFIG_SUMMARY = f"""
╔════════════════════════════════════════════════════════════════╗
║           API CONFIGURATION SUMMARY                            ║
╚════════════════════════════════════════════════════════════════╝

SERVER:
  Host: {API_HOST}
  Port: {API_PORT}
  Workers: {API_WORKERS}
  Reload: {API_RELOAD}

SERVICES:
  Weaviate: {WEAVIATE_URL}
  Claude: {CLAUDE_MODEL}
  
RATE LIMITS:
  Project Analysis: {RATE_LIMIT_ANALYZE_PROJECT} req/min
  Contract Analysis: {RATE_LIMIT_ANALYZE_CONTRACT} req/min
  Search: {RATE_LIMIT_SEARCH} req/min
  General: {RATE_LIMIT_GENERAL} req/min

FEATURES:
  Contract Analysis: {FEATURE_CONTRACT_ANALYSIS}
  Project Analysis: {FEATURE_PROJECT_ANALYSIS}
  Regulation Search: {FEATURE_SEARCH}
  Enforcement Cases: {FEATURE_ENFORCEMENT_CASES}
"""
