# from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.config import settings
from src.exceptions import InvalidAPIKeyError


def validate_api_key(api_key: str) -> None:
    """Validate API key against configured keys"""
    if not api_key:
        raise InvalidAPIKeyError("API key is required")

    if api_key not in settings.valid_api_keys:
        raise InvalidAPIKeyError("Invalid API key")

# Add this line for debugging