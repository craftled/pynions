from typing import Dict, Any
import os
from dotenv import load_dotenv
import json
from pathlib import Path

CONFIG_DIR = Path(__file__).parent.parent / "config"


class Config:
    """Centralized configuration management"""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        """Load all configuration from the central config directory"""
        # Load .env from config directory
        load_dotenv(CONFIG_DIR / ".env")

        # Load settings.json from config directory
        with open(CONFIG_DIR / "settings.json") as f:
            self.settings = json.load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get any config value (env or setting)"""
        return os.getenv(key) or self.settings.get(key, default)


# Global instance
config = Config()
