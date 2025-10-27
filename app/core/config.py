from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database settings
    mongodb_url: str = "mongodb://admin:password@localhost:27017/notes_api?authSource=admin"
    database_name: str = "notes_api"
    
    # Application settings
    app_name: str = "Multi-Tenant Notes API"
    app_version: str = "1.0.0"
    environment: str = "development"
    debug: bool = True
    
    # Security settings
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # CORS settings
    allowed_origins: list[str] = ["*"]
    allowed_methods: list[str] = ["*"]
    allowed_headers: list[str] = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()
