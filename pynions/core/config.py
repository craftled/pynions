"""Simple configuration management for Pynions"""

import os
from pathlib import Path
from dotenv import load_dotenv
import json

class Config:
    """Minimal configuration management"""

    _instance = None
    _default_config = {
        "save_results": True,
        "output_folder": "data"
    }

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        """Load configuration from root directory"""
        self.settings = self._default_config.copy()
        
        # Load .env from root
        root = Path(__file__).parent.parent.parent
        env_path = root / ".env"
        if env_path.exists():
            load_dotenv(env_path)
        
        # Load optional pynions.json
        config_path = root / "pynions.json"
        if config_path.exists():
            try:
                with open(config_path) as f:
                    self.settings.update(json.load(f))
            except Exception as e:
                print(f"⚠️  Note: Using default settings ({str(e)})")

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value (env vars take priority)"""
        return os.getenv(key.upper()) or self.settings.get(key, default)

    def check_api_key(self, key: str = "OPENAI_API_KEY") -> bool:
        """Check if API key exists"""
        if not os.getenv(key):
            print(f"❌ Missing {key}! Add it to your .env file")
            print("💡 Tip: Copy .env.example to .env and add your key")
            return False
        return True

# Global instance
config = Config()
