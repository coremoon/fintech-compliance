"""
Configuration management for fintech-compliance
"""

import os
from pathlib import Path
from dotenv import load_dotenv

# Project root (FIRST, so we can use it for .env path)
PROJECT_ROOT = Path(__file__).parent.parent

# Load environment variables from explicit path
ENV_FILE = PROJECT_ROOT / ".env"
load_dotenv(dotenv_path=ENV_FILE, override=True)

# Claude API
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-5-20250929")

# Weaviate
WEAVIATE_URL = os.getenv("WEAVIATE_URL", "http://localhost:8080")
WEAVIATE_API_KEY = os.getenv("WEAVIATE_API_KEY", "2022weaviate")

# Data paths
DATA_PATH = Path(os.getenv("DATA_PATH", PROJECT_ROOT / "data"))
REGULATORY_DB_PATH = Path(os.getenv("REGULATORY_DB_PATH", DATA_PATH / "regulatory"))
CASE_LAW_PATH = Path(os.getenv("CASE_LAW_PATH", DATA_PATH / "cases"))
TECH_SPECS_PATH = Path(os.getenv("TECH_SPECS_PATH", DATA_PATH / "tech"))

# API Configuration
API_HOST = os.getenv("API_HOST", "0.0.0.0")
API_PORT = int(os.getenv("API_PORT", 8000))
API_LOG_LEVEL = os.getenv("API_LOG_LEVEL", "INFO")

# MLflow
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
MLFLOW_EXPERIMENT_NAME = os.getenv("MLFLOW_EXPERIMENT_NAME", "fintech-compliance-dev")

# Development
DEBUG = os.getenv("DEBUG", "false").lower() == "true"
VERBOSE = os.getenv("VERBOSE", "true").lower() == "true"

# Ensure directories exist
for path in [REGULATORY_DB_PATH, CASE_LAW_PATH, TECH_SPECS_PATH]:
    path.mkdir(parents=True, exist_ok=True)

if __name__ == "__main__":
    print(f"Project Root: {PROJECT_ROOT}")
    print(f"Weaviate: {WEAVIATE_URL}")
    print(f"Claude Model: {ANTHROPIC_MODEL}")
    print(f"Data Path: {DATA_PATH}")
