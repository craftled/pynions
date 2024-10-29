from datetime import datetime, timedelta
from typing import Dict, Optional


class RateLimiter:
    def __init__(self, calls_per_minute: int = 60):
        self.calls_per_minute = calls_per_minute
        self.calls: Dict[str, list[datetime]] = {}

    async def wait_if_needed(self, key: str = "default") -> None:
        """Wait if we've exceeded our rate limit"""
        now = datetime.now()
        minute_ago = now - timedelta(minutes=1)

        if key not in self.calls:
            self.calls[key] = []

        # Clean old calls
        self.calls[key] = [t for t in self.calls[key] if t > minute_ago]

        # Wait if needed
        if len(self.calls[key]) >= self.calls_per_minute:
            wait_time = (self.calls[key][0] - minute_ago).total_seconds()
            if wait_time > 0:
                import asyncio

                await asyncio.sleep(wait_time)
                # Recursive call to ensure we're now under limit
                await self.wait_if_needed(key)

        # Add current call
        self.calls[key].append(now)
