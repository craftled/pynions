from typing import Dict, Any, List, Optional
from .base import BaseTool


class Workflow:
    """Core workflow class for automation"""

    def __init__(self, name: Optional[str] = None):
        self.name = name or self.__class__.__name__
        self.tools: List[BaseTool] = []
        self.state: Dict[str, Any] = {}

    def add(self, tool: BaseTool) -> "Workflow":
        """Add a tool to the workflow"""
        self.tools.append(tool)
        return self

    async def run(self, input_data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Run the workflow"""
        print(f"\n🚀 Starting workflow: {self.name}")
        self.state = input_data or {}

        for tool in self.tools:
            try:
                print(f"\n⚙️  Running: {tool.__class__.__name__}")
                self.state = await tool.run(self.state)
            except Exception as e:
                print(f"❌ Error in {tool.__class__.__name__}: {str(e)}")
                raise

        print(f"\n✅ Workflow completed: {self.name}")
        return self.state
