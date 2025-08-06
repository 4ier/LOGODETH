#!/usr/bin/env python3
"""
Railway-optimized startup script for LOGODETH
"""
import os
import sys
import uvicorn
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent))

# Set minimal required environment variables if missing
if not os.getenv("LOGODETH_OPENAI_API_KEY"):
    os.environ["LOGODETH_OPENAI_API_KEY"] = "not-set"

if not os.getenv("LOGODETH_REDIS_URL"):
    os.environ["LOGODETH_REDIS_URL"] = "redis://localhost:6379"

if not os.getenv("LOGODETH_ENVIRONMENT"):
    os.environ["LOGODETH_ENVIRONMENT"] = "production"

# Get port from Railway
port = int(os.getenv("PORT", 8000))

if __name__ == "__main__":
    print("🚀 Starting LOGODETH API on Railway...")
    print(f"   Port: {port}")
    print(f"   Environment: {os.getenv('LOGODETH_ENVIRONMENT', 'unknown')}")
    
    try:
        uvicorn.run(
            "backend.app:app",
            host="0.0.0.0",
            port=port,
            log_level="info",
            access_log=True
        )
    except Exception as e:
        print(f"❌ Failed to start: {e}")
        sys.exit(1)