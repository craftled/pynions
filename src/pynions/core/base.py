from abc import ABC, abstractmethod
from typing import Dict, Any


class BaseTool(ABC):
    """Base class for all tools (both core and custom)"""

    @abstractmethod
    async def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the tool"""
        pass
