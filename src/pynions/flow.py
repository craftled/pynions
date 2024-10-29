from typing import Any, Dict, List, Union, Callable
from .core.base import BaseTool


class Flow:
    def __init__(self):
        self.steps: List[Union[BaseTool, Callable]] = []
        self.data: Dict[str, Any] = {}

    def add_step(self, step: Union[BaseTool, Callable]):
        """Add a step (tool or function) to the flow"""
        self.steps.append(step)
        return self

    async def run(self, initial_data: Dict[str, Any] = None):
        """Run all steps in the flow"""
        if initial_data:
            self.data.update(initial_data)

        for step in self.steps:
            if isinstance(step, BaseTool):
                result = await step.run(self.data)
            else:  # Callable
                result = await step(self.data)

            if result:
                self.data.update(result)

        return self.data
