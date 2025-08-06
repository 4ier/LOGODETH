"""
Rate limiting and cost control utilities
"""
from typing import Optional
from datetime import datetime, timedelta
import asyncio
from collections import defaultdict
from loguru import logger

from backend.config import get_settings


class RateLimiter:
    """Simple in-memory rate limiter"""
    
    def __init__(self):
        self.settings = get_settings()
        self.requests = defaultdict(list)
        self.lock = asyncio.Lock()
        
    async def check_rate_limit(self, identifier: str) -> tuple[bool, Optional[int]]:
        """
        Check if request is within rate limit
        
        Args:
            identifier: Unique identifier (IP, API key, etc.)
            
        Returns:
            (allowed, seconds_until_reset)
        """
        async with self.lock:
            now = datetime.now()
            minute_ago = now - timedelta(minutes=1)
            
            # Clean old requests
            self.requests[identifier] = [
                req_time for req_time in self.requests[identifier]
                if req_time > minute_ago
            ]
            
            # Check limit
            if len(self.requests[identifier]) >= self.settings.api_rate_limit:
                oldest_request = min(self.requests[identifier])
                reset_time = oldest_request + timedelta(minutes=1)
                seconds_until_reset = int((reset_time - now).total_seconds())
                
                logger.warning(f"Rate limit exceeded for {identifier}")
                return False, seconds_until_reset
            
            # Add current request
            self.requests[identifier].append(now)
            return True, None


class CostTracker:
    """Track API usage costs"""
    
    def __init__(self):
        self.daily_costs = defaultdict(float)
        self.monthly_costs = defaultdict(float)
        self.lock = asyncio.Lock()
        
        # Approximate costs per API call
        self.costs = {
            "gpt-4-vision-preview": 0.03,
            "claude-3-opus-20240229": 0.025,
            "fallback": 0.01
        }
        
    async def add_usage(self, model: str, identifier: str = "default"):
        """Record API usage"""
        async with self.lock:
            cost = self.costs.get(model, 0.02)
            
            today = datetime.now().date().isoformat()
            month = datetime.now().strftime("%Y-%m")
            
            self.daily_costs[f"{identifier}:{today}"] += cost
            self.monthly_costs[f"{identifier}:{month}"] += cost
            
            logger.info(f"API usage recorded: {model} (${cost:.3f})")
            
    async def get_usage_stats(self, identifier: str = "default") -> dict:
        """Get usage statistics"""
        async with self.lock:
            today = datetime.now().date().isoformat()
            month = datetime.now().strftime("%Y-%m")
            
            return {
                "daily_cost": self.daily_costs.get(f"{identifier}:{today}", 0),
                "monthly_cost": self.monthly_costs.get(f"{identifier}:{month}", 0),
                "daily_requests": sum(
                    1 for k in self.daily_costs.keys() 
                    if k.startswith(f"{identifier}:{today}")
                ),
                "estimated_monthly": self.daily_costs.get(f"{identifier}:{today}", 0) * 30
            }
    
    async def check_budget_limit(self, identifier: str = "default", daily_limit: float = 10.0, monthly_limit: float = 100.0) -> tuple[bool, str]:
        """
        Check if within budget limits
        
        Returns:
            (within_budget, reason_if_exceeded)
        """
        stats = await self.get_usage_stats(identifier)
        
        if stats["daily_cost"] >= daily_limit:
            return False, f"Daily limit of ${daily_limit:.2f} exceeded"
        
        if stats["monthly_cost"] >= monthly_limit:
            return False, f"Monthly limit of ${monthly_limit:.2f} exceeded"
        
        return True, ""


# Global instances
rate_limiter = RateLimiter()
cost_tracker = CostTracker()