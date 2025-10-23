from pydantic_settings import BaseSettings
from pathlib import Path
from dotenv import load_dotenv


load_dotenv()


class Settings(BaseSettings):
    """Global application settings"""

    # Model paths
    YOLO_MODEL_PATH: str = "weights/icon_detect/model.pt"
    CAPTION_MODEL_NAME: str = "florence2"
    CAPTION_MODEL_PATH: str = "weights/icon_caption_florence"

    # API Keys (comma-separated for multiple keys)
    API_KEYS: str = "your-secret-key-here"

    # Parsing defaults
    DEFAULT_BOX_THRESHOLD: float = 0.05
    DEFAULT_IOU_THRESHOLD: float = 0.1
    DEFAULT_IMG_SIZE: int = 640

    # Project root
    PROJECT_ROOT: Path = Path(__file__).parent.parent

    class Config:
        env_file = ".env"
        case_sensitive = True

    @property
    def valid_api_keys(self) -> set[str]:
        """Parse comma-separated API keys into a set"""
        print(f"DEBUG: Raw API_KEYS = {repr(self.API_KEYS)}")  # Add this
        keys = {key.strip() for key in self.API_KEYS.split(",")}
        print(f"DEBUG: Parsed keys = {keys}")  # Add this
        return keys


settings = Settings()
