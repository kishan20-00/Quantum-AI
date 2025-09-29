import json
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

def setup_logging(level: str = "INFO"):
    """Setup basic logging configuration"""
    logging.basicConfig(
        level=getattr(logging, level.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def validate_api_key(api_key: str) -> bool:
    """Basic API key validation"""
    if not api_key or not isinstance(api_key, str):
        return False
    return len(api_key.strip()) > 0

def generate_request_id() -> str:
    """Generate a unique request ID"""
    import uuid
    return str(uuid.uuid4())