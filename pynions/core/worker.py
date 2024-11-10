from abc import ABC, abstractmethod
from typing import Dict, Any
import logging


class Worker(ABC):
    """Base class for all Pynions workers"""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.logger = logging.getLogger(self.__class__.__name__)

    @abstractmethod
    async def execute(self, input_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute the worker's task"""
        pass

    def validate_input(self, input_data: Dict[str, Any]) -> bool:
        """Validate input data"""
        return True  # Override in subclasses

    def validate_output(self, output: Dict[str, Any]) -> bool:
        """Validate output data"""
        return True  # Override in subclasses
