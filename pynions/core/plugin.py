from abc import ABC, abstractmethod
from typing import Any, Dict
import logging


class Plugin(ABC):
    """Base class for all plugins"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(f"pynions.{self.__class__.__name__}")

    @abstractmethod
    async def execute(self, input_data: Any) -> Any:
        """Execute the plugin's main functionality"""
        pass

    def validate_config(self) -> bool:
        """Validate plugin configuration"""
        return True
