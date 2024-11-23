"""Simple configuration management for Pynions"""

import os
from pathlib import Path
from dotenv import load_dotenv
import json
from typing import Any, Dict

class Config:
    """Minimal configuration management"""

    _instance = None
    _settings: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
        return cls._instance

    def load_env(self, env_path: Path) -> None:
        """Load environment variables from .env file"""
        if env_path.exists():
            load_dotenv(env_path)

    def load_json(self, config_path: Path) -> None:
        """Load JSON configuration from file"""
        if config_path.exists():
            with open(config_path) as f:
                self._settings.update(json.load(f))

    def get(self, key: str, default: Any = None) -> Any:
        """Get a configuration value"""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set a configuration value"""
        self._settings[key] = value

    def clear(self) -> None:
        """Clear all configuration values"""
        self._settings.clear()

    def load(self, env_path: Path = None, config_path: Path = None) -> None:
        """Load configuration from both .env and JSON files"""
        if env_path is not None:
            self.load_env(env_path)
        if config_path is not None:
            self.load_json(config_path)

    def _load(self, root_dir: Path = None) -> None:
        """Internal method to load configuration from default paths"""
        if root_dir is None:
            root_dir = Path(__file__).parent.parent.parent

        env_path = root_dir / ".env"
        config_path = root_dir / "pynions.json"

        self.load(env_path, config_path)

# Global instance
config = Config()
config._load()
