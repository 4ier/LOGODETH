"""
Redis cache service for recognition results
"""
import json
import hashlib
from typing import Optional, Dict, Any
import redis.asyncio as redis
from loguru import logger
from datetime import datetime, timedelta

from backend.config import get_settings


class ImageHasher:
    """Utility class for generating image hashes"""
    
    @staticmethod
    def hash_image(image_bytes: bytes) -> str:
        """
        Generate SHA-256 hash of image bytes
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Hexadecimal hash string
        """
        return hashlib.sha256(image_bytes).hexdigest()
    
    @staticmethod
    def hash_image_with_params(image_bytes: bytes, **params) -> str:
        """
        Generate hash including processing parameters
        
        Args:
            image_bytes: Raw image bytes
            **params: Additional parameters to include in hash
            
        Returns:
            Hexadecimal hash string
        """
        # Create a combined string with image hash and sorted parameters
        image_hash = ImageHasher.hash_image(image_bytes)
        
        if params:
            param_str = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
            combined = f"{image_hash}:{param_str}"
            return hashlib.sha256(combined.encode()).hexdigest()
        
        return image_hash


class CacheService:
    """Redis-based caching service"""
    
    def __init__(self):
        self.settings = get_settings()
        self.redis_client = None
        self.prefix = "logodeth:logo:"
        self.hasher = ImageHasher()
    
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
    
    async def get_by_image(self, image_bytes: bytes, **params) -> Optional[Dict[str, Any]]:
        """
        Get cached result by image bytes
        
        Args:
            image_bytes: Raw image bytes
            **params: Additional parameters used in processing
            
        Returns:
            Cached data or None
        """
        image_hash = self.hasher.hash_image_with_params(image_bytes, **params)
        return await self.get(image_hash)
    
    async def set_by_image(self, image_bytes: bytes, value: Dict[str, Any], **params) -> bool:
        """
        Set cached result by image bytes
        
        Args:
            image_bytes: Raw image bytes
            value: Data to cache
            **params: Additional parameters used in processing
            
        Returns:
            Success status
        """
        image_hash = self.hasher.hash_image_with_params(image_bytes, **params)
        
        # Add metadata to cached value
        enhanced_value = {
            **value,
            "_cache_metadata": {
                "cached_at": datetime.utcnow().isoformat(),
                "image_hash": image_hash,
                "cache_params": params,
                "ttl_seconds": self.settings.cache_ttl
            }
        }
        
        return await self.set(image_hash, enhanced_value)
    
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
            
            # Enhance value with cache metadata if not already present
            if "_cache_metadata" not in value:
                value = {
                    **value,
                    "_cache_metadata": {
                        "cached_at": datetime.utcnow().isoformat(),
                        "cache_key": key,
                        "ttl_seconds": self.settings.cache_ttl
                    }
                }
            
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
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get cache statistics
        
        Returns:
            Cache statistics
        """
        try:
            client = await self._get_client()
            pattern = f"{self.prefix}*"
            
            # Count keys
            key_count = 0
            total_memory = 0
            oldest_key = None
            newest_key = None
            
            async for key in client.scan_iter(match=pattern):
                key_count += 1
                
                # Get TTL for age calculation
                ttl = await client.ttl(key)
                if ttl > 0:
                    # Calculate age based on TTL
                    age = self.settings.cache_ttl - ttl
                    if oldest_key is None or age > oldest_key[1]:
                        oldest_key = (key, age)
                    if newest_key is None or age < newest_key[1]:
                        newest_key = (key, age)
            
            # Get Redis info
            info = await client.info()
            
            return {
                "total_keys": key_count,
                "redis_memory_used": info.get("used_memory_human", "unknown"),
                "redis_connected_clients": info.get("connected_clients", 0),
                "oldest_entry_age_seconds": oldest_key[1] if oldest_key else None,
                "newest_entry_age_seconds": newest_key[1] if newest_key else None,
                "cache_ttl_seconds": self.settings.cache_ttl,
                "hit_rate": "Not implemented",  # Would need separate tracking
            }
            
        except Exception as e:
            logger.error(f"Cache stats error: {e}")
            return {"error": str(e)}
    
    async def close(self):
        """Close Redis connection"""
        if self.redis_client:
            await self.redis_client.close()
            self.redis_client = None