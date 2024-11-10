from typing import Dict, Any
from .config import config


class Plugin:
    """Base plugin class"""

    def __init__(self, plugin_config: Dict[str, Any] = None):
        self.config = plugin_config or {}

    def get_env(self, key: str) -> str:
        """Get environment variable through core config"""
        return config.get_env(key)

    def get_setting(self, path: str) -> Any:
        """Get setting through core config"""
        return config.get_setting(path)
