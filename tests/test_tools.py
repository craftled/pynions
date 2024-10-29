import asyncio

import pytest

from pynions.tools import Cache, RateLimiter


def test_cache():
    """Test cache functionality"""
    cache = Cache(ttl=1)

    # Set and get
    cache.set("test", {"data": "value"})
    assert cache.get("test") == {"data": "value"}

    # TTL
    cache.set("expire", "value", ttl=0)
    assert cache.get("expire") is None


@pytest.mark.asyncio
async def test_rate_limiter():
    """Test rate limiting"""
    limiter = RateLimiter(rate=2)  # 2 requests per period

    # First two should be immediate
    assert await limiter.acquire()
    assert await limiter.acquire()

    # Third should timeout
    assert not await limiter.acquire(timeout=0.1)
