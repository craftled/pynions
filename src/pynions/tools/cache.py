from datetime import datetime
from typing import Any, Dict, Optional


class Cache:
    """Simple in-memory cache with TTL"""

    def __init__(self, ttl: int = 3600):
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set cache value with TTL"""
        expires = datetime.now().timestamp() + (ttl if ttl is not None else self.ttl)
        self._cache[key] = {"value": value, "expires": expires}

    def get(self, key: str) -> Optional[Any]:
        """Get cache value if not expired"""
        if key not in self._cache:
            return None

        data = self._cache[key]
        if data["expires"] <= datetime.now().timestamp():
            del self._cache[key]
            return None

        return data["value"]
