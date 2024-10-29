import asyncio
import time
from collections import deque
from typing import Optional


class RateLimiter:
    """
    Token bucket rate limiter.

    Example:
        ```python
        limiter = RateLimiter(60)  # 60 requests per minute
        async with limiter:
            # make api call
        ```
    """

    def __init__(self, rate: int, period: int = 60):
        self.rate = rate
        self.period = period
        self.tokens = deque()
        self._last_update = time.time()
        self._lock = asyncio.Lock()

    def _cleanup(self):
        """Remove expired tokens"""
        now = time.time()
        while self.tokens and self.tokens[0] < now - self.period:
            self.tokens.popleft()

    async def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire a token, waiting if necessary.

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            True if token acquired, False if timeout
        """
        start_time = time.time()

        async with self._lock:
            while True:
                self._cleanup()

                if len(self.tokens) < self.rate:
                    self.tokens.append(time.time())
                    return True

                # Check timeout
                if timeout is not None:
                    if time.time() - start_time >= timeout:
                        return False

                # Wait until oldest token expires
                sleep_time = self.tokens[0] - time.time() + self.period
                if sleep_time > 0:
                    await asyncio.sleep(min(sleep_time, timeout or sleep_time))

    async def __aenter__(self):
        """Async context manager support"""
        await self.acquire()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup on exit"""
        pass
