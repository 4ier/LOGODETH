#!/usr/bin/env python3
"""
Railway-optimized main entry point for LOGODETH
"""
import os
import sys
import uvicorn
from pathlib import Path

# Ensure backend is in path
sys.path.insert(0, str(Path(__file__).parent))

# Import after path setup
from backend.app import app

if __name__ == "__main__":
    # Get port from Railway (required)
    port = int(os.environ.get("PORT", 8000))
    
    print(f"🚀 Starting LOGODETH API...")
    print(f"   Port: {port}")
    print(f"   Environment: {os.environ.get('LOGODETH_ENVIRONMENT', 'production')}")
    
    # Run the app
    uvicorn.run(
        app,  # Direct app import instead of string
        host="0.0.0.0",  # Required for Railway
        port=port,
        log_level="info",
        access_log=True
    )