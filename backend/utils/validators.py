"""
File validation utilities
"""
from fastapi import UploadFile, HTTPException
import magic
from pathlib import Path
from loguru import logger


async def validate_image_file(file: UploadFile, settings) -> None:
    """
    Validate uploaded image file
    
    Checks:
    - File extension
    - File size
    - MIME type
    """
    # Check file extension
    if file.filename:
        ext = Path(file.filename).suffix.lower()
        if ext not in settings.allowed_extensions:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_file_type",
                    "message": f"File type {ext} not allowed. Allowed types: {', '.join(settings.allowed_extensions)}"
                }
            )
    
    # Check file size
    content = await file.read()
    file_size = len(content)
    
    if file_size > settings.max_file_size:
        raise HTTPException(
            status_code=413,
            detail={
                "error": "file_too_large",
                "message": f"File size {file_size/1024/1024:.1f}MB exceeds maximum allowed size of {settings.max_file_size/1024/1024}MB"
            }
        )
    
    # Check MIME type
    try:
        mime_type = magic.from_buffer(content, mime=True)
        allowed_mimes = ["image/jpeg", "image/png", "image/gif", "image/webp"]
        
        if mime_type not in allowed_mimes:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "invalid_mime_type",
                    "message": f"Invalid file type detected: {mime_type}"
                }
            )
    except Exception as e:
        logger.warning(f"Failed to check MIME type: {e}")
    
    # Reset file position
    await file.seek(0)
    
    logger.debug(f"File validation passed: {file.filename} ({file_size/1024:.1f}KB, {mime_type})")