"""
IndusMind AI — Redis Infrastructure

Async Redis client for caching and pub/sub.
"""

from __future__ import annotations

import redis.asyncio as aioredis

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)


class RedisClient:
    """Async Redis wrapper for caching and session management."""

    def __init__(self) -> None:
        self._client: aioredis.Redis | None = None

    async def connect(self) -> None:
        """Establish Redis connection."""
        if settings.DEMO_MODE:
            logger.info("Redis: Running in demo mode (in-memory fallback)")
            return
        try:
            self._client = aioredis.from_url(
                settings.REDIS_URL,
                encoding="utf-8",
                decode_responses=True,
                max_connections=20,
            )
            await self._client.ping()
            logger.info("Redis: Connected successfully")
        except Exception as e:
            logger.warning("Redis: Connection failed, using fallback", error=str(e))
            self._client = None

    async def disconnect(self) -> None:
        """Close Redis connection."""
        if self._client:
            await self._client.close()

    async def get(self, key: str) -> str | None:
        """Get value by key."""
        if not self._client:
            return None
        return await self._client.get(key)

    async def set(self, key: str, value: str, expire: int = 3600) -> None:
        """Set key-value with TTL."""
        if not self._client:
            return
        await self._client.set(key, value, ex=expire)

    async def delete(self, key: str) -> None:
        """Delete key."""
        if not self._client:
            return
        await self._client.delete(key)

    async def exists(self, key: str) -> bool:
        """Check if key exists."""
        if not self._client:
            return False
        return bool(await self._client.exists(key))


# Singleton
redis_client = RedisClient()
