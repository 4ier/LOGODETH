#!/usr/bin/env python
"""
Development server runner
"""
import uvicorn
from backend.config import get_settings

if __name__ == "__main__":
    settings = get_settings()
    
    uvicorn.run(
        "backend.app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.reload,
        log_level=settings.log_level.lower()
    )