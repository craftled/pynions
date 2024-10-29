from asyncio import Lock, sleep
from datetime import datetime
from typing import List, Optional
from collections import deque
import time
import asyncio


class RateLimiter:
    """Simple token bucket rate limiter"""

    def __init__(self, rate: int = 10, period: int = 60):
        """
        Initialize rate limiter

        Args:
            rate: Number of tokens per period
            period: Period in seconds
        """
        self.rate: int = rate
        self.period: int = period
        self.tokens: deque[float] = deque()
        self.lock: Lock = Lock()
        self._last_update: float = time.time()
        self._lock = asyncio.Lock()

    def _cleanup(self) -> None:
        """Remove expired tokens"""
        now = time.time()
        while self.tokens and self.tokens[0] < now - self.period:
            self.tokens.popleft()

    async def acquire(self, timeout: Optional[float] = None) -> bool:
        """
        Acquire a token if available

        Args:
            timeout: Maximum time to wait in seconds

        Returns:
            bool: True if token acquired, False if timeout
        """
        async with self.lock:
            self._cleanup()

            if len(self.tokens) >= self.rate:
                if timeout == 0:
                    return False

                sleep_time = self.tokens[0] - time.time() + self.period
                if timeout is not None and sleep_time > timeout:
                    return False

                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                self._cleanup()

            self.tokens.append(time.time())
            return True
