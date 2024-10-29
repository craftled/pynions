from abc import ABC, abstractmethod
from typing import Dict, Any
from rich import print as rprint


class BaseTool(ABC):
    """Base class for all tools"""

    def __init__(self, debug: bool = False):
        self.debug = debug

    @abstractmethod
    async def run(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Run the tool with the given data"""
        if self.debug:
            rprint(f"[dim]Tool input:[/] {data}")
        pass
