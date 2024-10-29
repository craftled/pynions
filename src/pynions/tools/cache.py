import json
from typing import Any, Optional
from pathlib import Path
import time
import hashlib


class Cache:
    """
    Simple file-based cache with TTL.

    Example:
        ```python
        cache = Cache(ttl=3600)
        cache.set("key", {"data": "value"})
        data = cache.get("key")
        ```
    """

    def __init__(self, ttl: int = 3600, directory: str = ".cache"):
        self.ttl = ttl
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)

    def _hash_key(self, key: str) -> str:
        """Create hash of cache key"""
        return hashlib.md5(key.encode()).hexdigest()

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        path = self.directory / f"{self._hash_key(key)}.json"
        if not path.exists():
            return None

        try:
            data = json.loads(path.read_text())
            if data["expires"] < time.time():
                path.unlink()
                return None
            return data["value"]
        except:
            return None

    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> None:
        """Set value in cache"""
        path = self.directory / f"{self._hash_key(key)}.json"
        data = {"value": value, "expires": time.time() + (ttl or self.ttl)}
        path.write_text(json.dumps(data))

    def clear(self, pattern: Optional[str] = None) -> None:
        """Clear cache entries"""
        for path in self.directory.glob("*.json"):
            if pattern is None or pattern in path.stem:
                path.unlink()
