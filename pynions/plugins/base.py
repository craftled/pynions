from abc import ABC, abstractmethod


class Plugin(ABC):
    """Base class for all plugins"""

    def __init__(self, config=None):
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
