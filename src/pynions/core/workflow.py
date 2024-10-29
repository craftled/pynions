from typing import Dict, Any
from .base import BaseTool


class Workflow:
    """Core workflow class for automation"""

    def __init__(self, name: str):
        self.name = name
        self.tools = []

    def add(self, tool: BaseTool):
        """Add a tool to the workflow"""
        self.tools.append(tool)
        return self  # Enable chaining

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the workflow"""
        current_context = context.copy()  # Start with input context

        # Process through each tool in sequence
        for tool in self.tools:
            # Run current tool and get its result
            tool_result = await tool.run(current_context)

            # Update context with tool's result
            # This ensures each subsequent tool gets the full context
            current_context.update(tool_result)

            # For debugging
            # print(f"After {tool.__class__.__name__}: {current_context}")

        return current_context
