from typing import Dict, Any
from rich import print as rprint
from .base import BaseTool


class Workflow:
    """Core workflow class for automation"""

    def __init__(self, name: str, debug: bool = False):
        self.name = name
        self.tools = []
        self.debug = debug
        if self.debug:
            rprint(f"[bold green]🔧 Initializing workflow:[/] {name}")

    def add(self, tool: BaseTool):
        """Add a tool to the workflow"""
        if self.debug:
            rprint(f"[bold blue]➕ Adding tool:[/] {tool.__class__.__name__}")
        self.tools.append(tool)
        return self  # Enable chaining

    async def run(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Run the workflow"""
        if self.debug:
            rprint(f"\n[bold yellow]🚀 Starting workflow:[/] {self.name}")
            rprint(f"[dim]Initial context:[/] {context}")

        current_context = context.copy()

        for tool in self.tools:
            if self.debug:
                rprint(f"\n[bold cyan]⚙️ Running tool:[/] {tool.__class__.__name__}")

            try:
                tool_result = await tool.run(current_context)
                current_context.update(tool_result)

                if self.debug:
                    rprint(f"[dim]Updated context:[/] {current_context}")
            except Exception as e:
                rprint(
                    f"[bold red]❌ Error in tool {tool.__class__.__name__}:[/] {str(e)}"
                )
                raise

        if self.debug:
            rprint(f"\n[bold green]✅ Workflow complete:[/] {self.name}")

        return current_context
