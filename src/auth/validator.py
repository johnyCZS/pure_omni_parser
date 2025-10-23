from dotenv import load_dotenv
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.exceptions import InvalidAPIKeyError


class Validator:
    def __init__(self):
        self.api_key = None

        if not load_dotenv(".env"):
            raise FileNotFoundError("'.env' file not found or could not be loaded.")

        self.api_key = os.getenv("API_KEYS")

    def validate(self, incoming_api_key: str):
        if incoming_api_key != self.api_key:
            raise InvalidAPIKeyError("The provided API key is invalid.")
        return True
