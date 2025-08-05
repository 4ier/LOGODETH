"""
Configuration management for LOGODETH API
"""
from typing import List, Optional
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings"""
    
    # API Keys
    openai_api_key: str
    anthropic_api_key: Optional[str] = None
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    cache_ttl: int = 86400  # 24 hours
    
    # API Configuration
    api_rate_limit: int = 10  # requests per minute
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_extensions: List[str] = [".jpg", ".jpeg", ".png", ".gif", ".webp"]
    
    # CORS Settings
    cors_origins: List[str] = ["http://localhost:8000", "http://localhost:3000"]
    
    # Logging
    log_level: str = "INFO"
    
    # Development
    debug: bool = False
    reload: bool = True
    
    # Optional Services
    sentry_dsn: Optional[str] = None
    posthog_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()