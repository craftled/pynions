from pathlib import Path
import json
from dotenv import load_dotenv

CONFIG_DIR = Path(__file__).parent
DEFAULT_CONFIG_PATH = CONFIG_DIR / "settings.json"
ENV_PATH = CONFIG_DIR / ".env"


def load_config(custom_config=None):
    """Load configuration from files and merge with custom config"""
    # Load environment variables
    load_dotenv(ENV_PATH)

    # Load default settings
    with open(DEFAULT_CONFIG_PATH) as f:
        config = json.load(f)

    # Merge with custom config
    if custom_config:
        config.update(custom_config)

    return config
