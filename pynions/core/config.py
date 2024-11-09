import json
import logging
from typing import Any, Dict
from pathlib import Path


class Config:
    """Manages configuration loading and access"""

    def __init__(self, config_file: str = "settings.json"):
        self.config_dir = Path(__file__).parent.parent / "config"
        self.config_file = self.config_dir / config_file
        self.config_data = {}
        self.logger = logging.getLogger("pynions.config")
        self._load_config()

    def _load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, "r") as f:
                self.config_data = json.load(f)
        except FileNotFoundError:
            self.logger.warning(
                f"Config file {self.config_file} not found, using defaults"
            )
        except json.JSONDecodeError:
            self.logger.error(f"Invalid JSON in {self.config_file}")
            raise

    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """Get configuration for a specific plugin"""
        return self.config_data.get("plugins", {}).get(plugin_name, {})
