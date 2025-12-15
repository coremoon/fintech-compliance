"""
Logging configuration for fintech-compliance
"""

import logging
import sys
from pathlib import Path
from src.config import DEBUG, VERBOSE

# Create logs directory
LOGS_DIR = Path(__file__).parent.parent.parent / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# Configure logger
logger = logging.getLogger("fintech-compliance")
logger.setLevel(logging.DEBUG if DEBUG else logging.INFO)

# Console handler
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG if VERBOSE else logging.INFO)

# File handler
file_handler = logging.FileHandler(LOGS_DIR / "fintech-compliance.log")
file_handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter(
    "[%(asctime)s] %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

# Add handlers
logger.addHandler(console_handler)
logger.addHandler(file_handler)

if __name__ == "__main__":
    logger.debug("Debug message")
    logger.info("Info message")
    logger.warning("Warning message")
    logger.error("Error message")
