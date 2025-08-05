"""
Logo recognition API endpoints
"""
from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from fastapi.responses import JSONResponse
from typing import Optional
import time
from loguru import logger

from backend.config import get_settings
from backend.models.recognition import RecognitionResult, RecognitionError
from backend.services.recognition import RecognitionService
from backend.utils.validators import validate_image_file

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
    file: UploadFile = File(..., description="Logo image file"),
    service: RecognitionService = Depends(get_recognition_service)
) -> RecognitionResult:
    """
    Recognize a metal band logo using multimodal AI.
    
    Supports formats: JPG, PNG, GIF, WebP
    Max file size: 10MB
    """
    start_time = time.time()
    
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