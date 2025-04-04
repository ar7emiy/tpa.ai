# config/settings.py
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Default settings with fallbacks
SETTINGS = {
    # API credentials
    "GOOGLE_API_KEY": os.environ.get("GOOGLE_API_KEY", ""),
    
    # Database settings
    "SQLITE_DB_PATH": os.environ.get("SQLITE_DB_PATH", "wc_claims.db"),
    "CHROMADB_PATH": os.environ.get("CHROMADB_PATH", "chromadb"),
    
    # Logging
    "LOG_LEVEL": os.environ.get("LOG_LEVEL", "INFO"),
    
    # Model settings
    "DEFAULT_MODEL": os.environ.get("DEFAULT_MODEL", "gemini-2.0-pro"),
    "GENERATION_TEMPERATURE": float(os.environ.get("GENERATION_TEMPERATURE", "0.7")),
    
    # Workflow settings
    "MAX_PROCESSING_ATTEMPTS": int(os.environ.get("MAX_PROCESSING_ATTEMPTS", "3")),
}

def validate_settings():
    """Validate that required settings are present."""
    if not SETTINGS["GOOGLE_API_KEY"]:
        raise ValueError("GOOGLE_API_KEY environment variable is required")

# Validate settings on import
validate_settings()
