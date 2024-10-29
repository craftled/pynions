from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    """Base class for all tools"""

    @abstractmethod
    async def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the tool with input data, return updated state"""
        pass
