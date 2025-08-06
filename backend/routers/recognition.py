"""
Logo recognition API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from typing import Optional
import time
from loguru import logger

from backend.config import get_settings
from backend.models.recognition import RecognitionResult, RecognitionError
from backend.services.recognition import RecognitionService
from backend.utils.validators import validate_image_file
from backend.utils.rate_limiter import rate_limiter, cost_tracker

router = APIRouter()
settings = get_settings()


def get_recognition_service() -> RecognitionService:
    """Dependency to get recognition service"""
    return RecognitionService()


@router.post(
    "/recognize",
    response_model=RecognitionResult,
    responses={
        400: {"model": RecognitionError, "description": "Invalid input"},
        413: {"model": RecognitionError, "description": "File too large"},
        500: {"model": RecognitionError, "description": "Internal server error"}
    },
    summary="Recognize metal band logo",
    description="Upload a metal band logo image and get the band name using AI"
)
async def recognize_logo(
    request: Request,
    file: UploadFile = File(..., description="Logo image file"),
    service: RecognitionService = Depends(get_recognition_service)
) -> RecognitionResult:
    """
    Recognize a metal band logo using multimodal AI.
    
    Supports formats: JPG, PNG, GIF, WebP
    Max file size: 10MB
    """
    start_time = time.time()
    
    # Check rate limit
    client_ip = request.client.host
    allowed, wait_seconds = await rate_limiter.check_rate_limit(client_ip)
    
    if not allowed:
        raise HTTPException(
            status_code=429,
            detail={
                "error": "rate_limit_exceeded",
                "message": f"Too many requests. Please wait {wait_seconds} seconds.",
                "retry_after": wait_seconds
            },
            headers={"Retry-After": str(wait_seconds)}
        )
    
    # Check budget limits (optional)
    within_budget, reason = await cost_tracker.check_budget_limit()
    if not within_budget:
        logger.warning(f"Budget limit exceeded: {reason}")
        raise HTTPException(
            status_code=402,
            detail={
                "error": "budget_exceeded",
                "message": reason,
                "suggestion": "Please wait until tomorrow or increase budget limits"
            }
        )
    
    try:
        # Validate file
        await validate_image_file(file, settings)
        
        # Read file content
        content = await file.read()
        
        # Process recognition
        logger.info(f"Processing logo recognition for file: {file.filename}")
        result = await service.recognize_logo(content, file.filename)
        
        # Add processing time
        result.processing_time = time.time() - start_time
        
        logger.info(f"Recognition completed in {result.processing_time:.2f}s")
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Recognition failed: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail={"error": "recognition_failed", "message": str(e)}
        )
    finally:
        # Clean up
        await file.close()


@router.get(
    "/recognize/{image_hash}",
    response_model=RecognitionResult,
    summary="Get cached recognition result",
    description="Retrieve a previously cached recognition result by image hash"
)
async def get_cached_result(
    image_hash: str,
    service: RecognitionService = Depends(get_recognition_service)
) -> RecognitionResult:
    """Get cached recognition result by image hash"""
    result = await service.get_cached_result(image_hash)
    
    if not result:
        raise HTTPException(
            status_code=404,
            detail={"error": "not_found", "message": "No cached result found"}
        )
    
    return result


@router.get(
    "/stats/usage",
    summary="Get API usage statistics",
    description="Get current API usage and cost statistics"
)
async def get_usage_stats():
    """Get usage statistics and costs"""
    stats = await cost_tracker.get_usage_stats()
    
    return {
        "usage": {
            "daily_cost": f"${stats['daily_cost']:.2f}",
            "monthly_cost": f"${stats['monthly_cost']:.2f}",
            "daily_requests": stats['daily_requests'],
            "estimated_monthly": f"${stats['estimated_monthly']:.2f}"
        },
        "limits": {
            "rate_limit": f"{settings.api_rate_limit} requests/minute",
            "daily_budget": "$10.00",
            "monthly_budget": "$100.00"
        },
        "cache_info": {
            "ttl": f"{settings.cache_ttl} seconds",
            "type": "Redis"
        }
    }