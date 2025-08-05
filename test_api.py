#!/usr/bin/env python3
"""
Quick API test script
"""
import asyncio
import httpx

async def test_api():
    """Test API endpoints"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        # Test health check
        print("🔍 Testing health check...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"✅ Health check: {response.status_code}")
            print(f"   Response: {response.json()}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
            return
        
        # Test API docs
        print("\n🔍 Testing API docs...")
        try:
            response = await client.get(f"{base_url}/docs")
            print(f"✅ API docs: {response.status_code}")
        except Exception as e:
            print(f"❌ API docs failed: {e}")
        
        print(f"\n🚀 API server is running at {base_url}")
        print(f"📖 API documentation: {base_url}/docs")
        print(f"🎯 Ready to test logo recognition!")

if __name__ == "__main__":
    asyncio.run(test_api())