"""Configuration management for the self-building system."""
import os
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # OpenAI Configuration
    openai_api_key: str
    openai_model: str = "gpt-4.1-mini"
    openai_temperature: float = 0.0
    
    # System Paths
    project_root: Path = Path(__file__).parent.parent.parent
    backend_root: Path = Path(__file__).parent.parent
    memory_dir: Path = backend_root / "memory"
    
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Ensure memory directory exists
        self.memory_dir.mkdir(parents=True, exist_ok=True)


# Global settings instance
settings = Settings()

# Configuration for integration with qbitz-backend
INTEGRATION_MODE = True
QBITZ_BACKEND_PATH = '../qbitz-backend'
