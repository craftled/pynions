"""
Simple file-based cache with TTL.
"""

import json
import time
from pathlib import Path
from typing import Any, Optional


class Cache:
    def __init__(self, ttl: int = 3600, directory: str = ".cache"):
        self.ttl = ttl
        self.directory = Path(directory)
        self.directory.mkdir(exist_ok=True)

    def get(self, key: str) -> Optional[Any]:
        """Get value from cache"""
        path = self.directory / f"{key}.json"
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

    def set(self, key: str, value: Any) -> None:
        """Set value in cache"""
        path = self.directory / f"{key}.json"
        data = {"value": value, "expires": time.time() + self.ttl}
        path.write_text(json.dumps(data))
