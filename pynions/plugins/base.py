from abc import ABC, abstractmethod
from dotenv import load_dotenv


class Plugin(ABC):
    """Base class for all plugins"""

    def __init__(self, config=None):
        load_dotenv()  # Load environment variables for all plugins
        self.config = config or {}

    @abstractmethod
    def initialize(self):
        """Initialize the plugin"""
        pass

    @abstractmethod
    def cleanup(self):
        """Cleanup plugin resources"""
        pass

    def validate_config(self):
        """Validate plugin configuration"""
        return True
