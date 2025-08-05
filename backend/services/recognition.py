"""
Logo recognition service using multimodal AI
"""
import base64
import hashlib
import json
from typing import Optional, Dict, Any
from datetime import datetime
import httpx
from loguru import logger

from backend.config import get_settings
from backend.models.recognition import RecognitionResult
from backend.services.cache import CacheService
from backend.services.llm_client import LLMClient


class RecognitionService:
    """Service for recognizing metal band logos"""
    
    def __init__(self):
        self.settings = get_settings()
        self.cache = CacheService()
        self.llm_client = LLMClient()
    
    async def recognize_logo(self, image_data: bytes, filename: str) -> RecognitionResult:
        """
        Recognize a metal band logo from image data
        
        Args:
            image_data: Raw image bytes
            filename: Original filename
            
        Returns:
            RecognitionResult with band information
        """
        # Calculate image hash for caching
        image_hash = self._calculate_image_hash(image_data)
        
        # Check cache first
        cached_result = await self.cache.get(image_hash)
        if cached_result:
            logger.info(f"Cache hit for image hash: {image_hash}")
            cached_result["cached"] = True
            return RecognitionResult(**cached_result)
        
        logger.info(f"Cache miss for image hash: {image_hash}, calling AI API")
        
        # Prepare image for API
        base64_image = base64.b64encode(image_data).decode('utf-8')
        
        # Try primary AI service (OpenAI)
        try:
            result = await self.llm_client.recognize_with_openai(base64_image)
            ai_model = "gpt-4-vision-preview"
        except Exception as e:
            logger.warning(f"OpenAI API failed: {e}, trying Anthropic")
            
            # Fallback to Anthropic if available
            if self.settings.anthropic_api_key:
                try:
                    result = await self.llm_client.recognize_with_anthropic(base64_image)
                    ai_model = "claude-3-opus-20240229"
                except Exception as e2:
                    logger.error(f"Both AI services failed: OpenAI: {e}, Anthropic: {e2}")
                    raise Exception("All AI services failed to process the image")
            else:
                raise e
        
        # Create recognition result
        recognition_result = RecognitionResult(
            band_name=result.get("band_name", "Unknown"),
            confidence=result.get("confidence", 0),
            genre=result.get("genre"),
            description=result.get("description"),
            ai_model=ai_model,
            cached=False,
            processing_time=0  # Will be set by the router
        )
        
        # Cache the result
        await self.cache.set(image_hash, recognition_result.model_dump())
        
        return recognition_result
    
    async def get_cached_result(self, image_hash: str) -> Optional[RecognitionResult]:
        """Get a cached recognition result by image hash"""
        cached_data = await self.cache.get(image_hash)
        if cached_data:
            cached_data["cached"] = True
            return RecognitionResult(**cached_data)
        return None
    
    def _calculate_image_hash(self, image_data: bytes) -> str:
        """Calculate SHA-256 hash of image data"""
        return hashlib.sha256(image_data).hexdigest()