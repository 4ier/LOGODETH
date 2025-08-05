"""
Redis cache service for recognition results
"""
import json
from typing import Optional, Dict, Any
import redis.asyncio as redis
from loguru import logger

from backend.config import get_settings


class CacheService:
    """Redis-based caching service"""
    
    def __init__(self):
        self.settings = get_settings()
        self.redis_client = None
        self.prefix = "logodeth:logo:"
    
    async def _get_client(self) -> redis.Redis:
        """Get or create Redis client"""
        if not self.redis_client:
            self.redis_client = redis.from_url(
                self.settings.redis_url,
                decode_responses=True
            )
        return self.redis_client
    
    async def get(self, key: str) -> Optional[Dict[str, Any]]:
        """
        Get cached value by key
        
        Args:
            key: Cache key (usually image hash)
            
        Returns:
            Cached data or None
        """
        try:
            client = await self._get_client()
            full_key = f"{self.prefix}{key}"
            
            value = await client.get(full_key)
            if value:
                logger.debug(f"Cache hit for key: {key}")
                return json.loads(value)
            
            logger.debug(f"Cache miss for key: {key}")
            return None
            
        except Exception as e:
            logger.error(f"Cache get error: {e}")
            # Don't fail if cache is down
            return None
    
    async def set(self, key: str, value: Dict[str, Any]) -> bool:
        """
        Set cache value with TTL
        
        Args:
            key: Cache key (usually image hash)
            value: Data to cache
            
        Returns:
            Success status
        """
        try:
            client = await self._get_client()
            full_key = f"{self.prefix}{key}"
            
            json_value = json.dumps(value, default=str)
            await client.setex(
                full_key,
                self.settings.cache_ttl,
                json_value
            )
            
            logger.debug(f"Cached result for key: {key} (TTL: {self.settings.cache_ttl}s)")
            return True
            
        except Exception as e:
            logger.error(f"Cache set error: {e}")
            # Don't fail if cache is down
            return False
    
    async def delete(self, key: str) -> bool:
        """
        Delete cached value
        
        Args:
            key: Cache key to delete
            
        Returns:
            Success status
        """
        try:
            client = await self._get_client()
            full_key = f"{self.prefix}{key}"
            
            result = await client.delete(full_key)
            logger.debug(f"Deleted cache key: {key}")
            return bool(result)
            
        except Exception as e:
            logger.error(f"Cache delete error: {e}")
            return False
    
    async def clear_all(self) -> int:
        """
        Clear all cached logos
        
        Returns:
            Number of keys deleted
        """
        try:
            client = await self._get_client()
            pattern = f"{self.prefix}*"
            
            # Find all keys matching pattern
            keys = []
            async for key in client.scan_iter(match=pattern):
                keys.append(key)
            
            # Delete all keys
            if keys:
                deleted = await client.delete(*keys)
                logger.info(f"Cleared {deleted} cached logos")
                return deleted
            
            return 0
            
        except Exception as e:
            logger.error(f"Cache clear error: {e}")
            return 0
    
    async def health_check(self) -> bool:
        """
        Check if Redis is healthy
        
        Returns:
            Health status
        """
        try:
            client = await self._get_client()
            await client.ping()
            return True
        except Exception as e:
            logger.error(f"Redis health check failed: {e}")
            return False
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None