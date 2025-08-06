#!/usr/bin/env python3
"""
Minimal test app for Railway deployment debugging
"""
import os
from fastapi import FastAPI
import uvicorn

# Create minimal FastAPI app
app = FastAPI(title="LOGODETH Test", version="1.0.0")

@app.get("/")
async def root():
    return {"status": "ok", "message": "Test app is running"}

@app.get("/health")
async def health():
    return {
        "status": "healthy", 
        "port": os.getenv("PORT", "unknown"),
        "env_vars": {
            "OPENROUTER_API_KEY": "set" if os.getenv("OPENROUTER_API_KEY") else "missing",
            "PORT": os.getenv("PORT", "missing"),
            "LOGODETH_ENVIRONMENT": os.getenv("LOGODETH_ENVIRONMENT", "missing")
        }
    }

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"🧪 Starting test app on port {port}")
    print(f"🔑 OPENROUTER_API_KEY: {'✅ Set' if os.getenv('OPENROUTER_API_KEY') else '❌ Missing'}")
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=port,
        log_level="debug"
    )