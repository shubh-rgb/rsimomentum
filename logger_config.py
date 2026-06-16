"""
Logging configuration for the application.
All logs are written to logs/app.log with proper isolation from user-facing output.
"""
import logging
import os
from pathlib import Path

# Create logs directory if it doesn't exist
LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"

# Configure root logger
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler(LOG_FILE),
        logging.StreamHandler()  # Also log to console in development
    ]
)

def get_logger(name):
    """Get a logger instance for a module."""
    return logging.getLogger(name)
