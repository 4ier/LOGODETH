"""
LOGODETH API - Metal Logo Recognition Engine
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
from loguru import logger

from backend.config import get_settings
from backend.routers import recognition
from backend.utils.logging import setup_logging

# Get settings
settings = get_settings()

# Setup logging
setup_logging(settings.log_level)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    logger.info("> LOGODETH API starting up...")
    logger.info(f"Debug mode: {settings.debug}")
    logger.info(f"Redis URL: {settings.redis_url}")
    
    yield
    
    # Shutdown
    logger.info("=y LOGODETH API shutting down...")


# Create FastAPI app
app = FastAPI(
    title="LOGODETH API",
    description="AI-powered metal band logo recognition",
    version="2.0.0",
    lifespan=lifespan,
    debug=settings.debug
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    recognition.router,
    prefix="/api/v1",
    tags=["recognition"]
)

# Health check endpoint
@app.get("/", tags=["health"])
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "LOGODETH API",
        "version": "2.0.0",
        "message": "> Ready to decode the undecipherable!"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "checks": {
            "api": "ok",
            "redis": "ok",  # TODO: Implement actual Redis health check
            "openai": "ok"  # TODO: Implement actual API health check
        }
    }