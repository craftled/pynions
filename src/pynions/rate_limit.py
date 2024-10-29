import asyncio
import time
from collections import deque


class RateLimiter:
    """
    Simple token bucket rate limiter.

    Example:
        ```python
        limiter = RateLimiter(60)  # 60 requests per minute
        await limiter.acquire()
        # make api call
        ```
    """

    def __init__(self, rate: int):
        self.rate = rate
        self.tokens = deque()
        self._last_update = time.time()

    def _cleanup(self):
        """Remove expired tokens"""
        now = time.time()
        while self.tokens and self.tokens[0] < now - 60:
            self.tokens.popleft()

    async def acquire(self):
        """Wait for rate limit"""
        self._cleanup()

        while len(self.tokens) >= self.rate:
            sleep_time = self.tokens[0] - time.time() + 60
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)
            self._cleanup()

        self.tokens.append(time.time())
