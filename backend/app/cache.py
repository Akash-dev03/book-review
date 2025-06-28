import redis.asyncio as redis
import json
from typing import Any, Optional
from app.config import settings

redis_client: Optional[redis.Redis] = None


async def init_cache():
    """Initialize Redis connection"""
    global redis_client
    redis_client = redis.from_url(settings.REDIS_URL, decode_responses=True)


async def get_cache(key: str) -> Optional[Any]:
    """Get value from cache"""
    try:
        if redis_client is None:
            return None
        
        value = await redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    except Exception as e:
        print(f"Cache get error: {e}")
        return None


async def set_cache(key: str, value: Any, ttl: int = settings.CACHE_TTL) -> bool:
    """Set value in cache"""
    try:
        if redis_client is None:
            return False
        
        await redis_client.setex(key, ttl, json.dumps(value, default=str))
        return True
    except Exception as e:
        print(f"Cache set error: {e}")
        return False


async def delete_cache(key: str) -> bool:
    """Delete value from cache"""
    try:
        if redis_client is None:
            return False
        
        await redis_client.delete(key)
        return True
    except Exception as e:
        print(f"Cache delete error: {e}")
        return False