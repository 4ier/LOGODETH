"""
Data models for logo recognition
"""
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class RecognitionResult(BaseModel):
    """Logo recognition result"""
    band_name: str = Field(..., description="Identified band name")
    confidence: float = Field(..., ge=0, le=100, description="Confidence score (0-100)")
    genre: Optional[str] = Field(None, description="Music genre")
    description: Optional[str] = Field(None, description="Brief description")
    ai_model: str = Field(..., description="AI model used for recognition")
    cached: bool = Field(False, description="Whether result was from cache")
    processing_time: float = Field(..., description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)


class RecognitionError(BaseModel):
    """Error response"""
    error: str = Field(..., description="Error type")
    message: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Additional details")


class HealthStatus(BaseModel):
    """Health check status"""
    status: str
    checks: dict