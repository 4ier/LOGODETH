"""
Configuration management for LOGODETH API

Provides centralized configuration with environment variable support,
validation, and development/production environment detection.
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import validator, Field
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings with validation and environment detection"""
    
    # Environment Detection
    environment: str = Field(default="development", description="Environment: development, production, testing")
    
    # API Keys and Base URLs
    openai_api_key: str = Field(..., description="OpenAI API key or OpenRouter API key")
    openai_base_url: Optional[str] = Field(default=None, description="Custom base URL for OpenAI-compatible APIs (e.g., OpenRouter)")
    anthropic_api_key: Optional[str] = Field(default=None, description="Anthropic API key for Claude Vision")
    anthropic_base_url: Optional[str] = Field(default=None, description="Custom base URL for Anthropic-compatible APIs")
    
    # Redis Configuration
    redis_url: str = Field(default="redis://localhost:6379", description="Redis connection URL")
    redis_password: Optional[str] = Field(default=None, description="Redis password if required")
    cache_ttl: int = Field(default=86400, ge=60, le=604800, description="Cache TTL in seconds (1min-7days)")
    cache_max_keys: int = Field(default=10000, ge=100, description="Maximum number of cache keys")
    
    # API Configuration
    host: str = Field(default="0.0.0.0", description="API server host")
    port: int = Field(default=8000, ge=1000, le=65535, description="API server port")
    api_rate_limit: int = Field(default=10, ge=1, le=1000, description="Requests per minute per IP")
    max_file_size: int = Field(default=10 * 1024 * 1024, ge=1024, le=50 * 1024 * 1024, description="Max file size in bytes")
    allowed_extensions: List[str] = Field(default=[".jpg", ".jpeg", ".png", ".gif", ".webp"], description="Allowed file extensions")
    
    # CORS Settings
    cors_origins: List[str] = Field(default_factory=lambda: ["http://localhost:8000", "http://localhost:3000", "http://127.0.0.1:8000"], description="Allowed CORS origins")
    
    # AI Provider Configuration
    openai_model: str = Field(default="gpt-4o", description="OpenAI model to use (or OpenRouter model like openai/gpt-4-vision-preview)")
    anthropic_model: str = Field(default="claude-3-5-sonnet-20241022", description="Anthropic model to use")
    use_openrouter: bool = Field(default=False, description="Enable OpenRouter integration")
    openrouter_site_url: Optional[str] = Field(default=None, description="Your site URL for OpenRouter (optional)")
    openrouter_app_name: Optional[str] = Field(default="LOGODETH", description="Your app name for OpenRouter (optional)")
    max_tokens: int = Field(default=300, ge=50, le=1000, description="Max tokens for AI responses")
    temperature: float = Field(default=0.1, ge=0.0, le=1.0, description="AI response temperature")
    ai_timeout: int = Field(default=60, ge=10, le=300, description="AI API timeout in seconds")
    
    # Logging
    log_level: str = Field(default="INFO", regex="^(DEBUG|INFO|WARNING|ERROR|CRITICAL)$", description="Log level")
    log_format: str = Field(default="json", regex="^(json|text)$", description="Log format")
    
    # Development Settings
    debug: bool = Field(default=False, description="Enable debug mode")
    reload: bool = Field(default=True, description="Enable auto-reload in development")
    
    # Security
    secret_key: str = Field(default_factory=lambda: os.urandom(32).hex(), description="Secret key for sessions/JWT")
    
    # Monitoring & Analytics
    sentry_dsn: Optional[str] = Field(default=None, description="Sentry DSN for error tracking")
    posthog_api_key: Optional[str] = Field(default=None, description="PostHog API key for analytics")
    
    # Performance
    worker_count: int = Field(default=1, ge=1, le=10, description="Number of worker processes")
    worker_timeout: int = Field(default=300, ge=30, le=3600, description="Worker timeout in seconds")
    
    @validator('environment')
    def validate_environment(cls, v):
        allowed = ['development', 'production', 'testing']
        if v not in allowed:
            raise ValueError(f'Environment must be one of: {", ".join(allowed)}')
        return v
    
    @validator('redis_url')
    def validate_redis_url(cls, v):
        if not v.startswith(('redis://', 'rediss://')):
            raise ValueError('Redis URL must start with redis:// or rediss://')
        return v
    
    @validator('cors_origins')
    def validate_cors_origins(cls, v):
        # Add common development origins if not present
        default_origins = [
            "http://localhost:8000",
            "http://localhost:3000", 
            "http://127.0.0.1:8000",
            "http://127.0.0.1:3000"
        ]
        for origin in default_origins:
            if origin not in v:
                v.append(origin)
        return v
    
    @property
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "production"
    
    @property
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == "development"
    
    @property
    def database_url(self) -> str:
        """Get database URL (future use)"""
        return os.getenv("DATABASE_URL", "")
    
    def get_redis_config(self) -> dict:
        """Get Redis configuration dict"""
        config = {
            "url": self.redis_url,
            "decode_responses": True,
            "socket_connect_timeout": 5,
            "socket_timeout": 5,
            "retry_on_timeout": True
        }
        if self.redis_password:
            config["password"] = self.redis_password
        return config
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        validate_assignment = True
        
        # Environment variable prefix
        env_prefix = "LOGODETH_"
        
        # Allow extra fields for future expansion
        extra = "allow"
        
        # Field documentation
        schema_extra = {
            "example": {
                "environment": "development",
                "openai_api_key": "sk-...",
                "anthropic_api_key": "sk-ant-...",
                "redis_url": "redis://localhost:6379",
                "debug": True,
                "log_level": "DEBUG"
            }
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()


def create_env_template() -> str:
    """Create .env template with all available settings"""
    template = '''# LOGODETH Environment Configuration
# Copy this file to .env and fill in your values

# Environment (development, production, testing)
LOGODETH_ENVIRONMENT=development

# Required: OpenAI API Key
LOGODETH_OPENAI_API_KEY=sk-your-openai-key-here

# Optional: Anthropic API Key (for Claude Vision fallback)
LOGODETH_ANTHROPIC_API_KEY=sk-ant-your-anthropic-key-here

# Redis Configuration
LOGODETH_REDIS_URL=redis://localhost:6379
LOGODETH_REDIS_PASSWORD=

# API Configuration
LOGODETH_HOST=0.0.0.0
LOGODETH_PORT=8000
LOGODETH_DEBUG=false
LOGODETH_API_RATE_LIMIT=10
LOGODETH_MAX_FILE_SIZE=10485760

# AI Models
LOGODETH_OPENAI_MODEL=gpt-4o
LOGODETH_ANTHROPIC_MODEL=claude-3-5-sonnet-20241022
LOGODETH_MAX_TOKENS=300
LOGODETH_TEMPERATURE=0.1

# Caching
LOGODETH_CACHE_TTL=86400
LOGODETH_CACHE_MAX_KEYS=10000

# Logging
LOGODETH_LOG_LEVEL=INFO
LOGODETH_LOG_FORMAT=json

# Optional: Monitoring
LOGODETH_SENTRY_DSN=
LOGODETH_POSTHOG_API_KEY=

# Security
LOGODETH_SECRET_KEY=your-secret-key-here
'''
    return template


def validate_required_settings() -> tuple[bool, list[str]]:
    """Validate that all required settings are present"""
    try:
        settings = get_settings()
        missing = []
        
        # Check required API keys
        if not settings.openai_api_key or settings.openai_api_key == "sk-your-openai-key-here":
            missing.append("LOGODETH_OPENAI_API_KEY")
        
        # Check Redis connection (in production)
        if settings.is_production and not settings.redis_url:
            missing.append("LOGODETH_REDIS_URL")
        
        return len(missing) == 0, missing
        
    except Exception as e:
        return False, [f"Configuration error: {str(e)}"]


def get_config_summary() -> dict:
    """Get a summary of current configuration (without secrets)"""
    settings = get_settings()
    
    return {
        "environment": settings.environment,
        "debug": settings.debug,
        "host": settings.host,
        "port": settings.port,
        "redis_configured": bool(settings.redis_url),
        "openai_configured": bool(settings.openai_api_key),
        "anthropic_configured": bool(settings.anthropic_api_key),
        "cache_ttl_hours": settings.cache_ttl // 3600,
        "max_file_size_mb": settings.max_file_size // 1024 // 1024,
        "log_level": settings.log_level,
        "cors_origins_count": len(settings.cors_origins),
        "monitoring_enabled": bool(settings.sentry_dsn or settings.posthog_api_key)
    }