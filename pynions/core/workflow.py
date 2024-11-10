from typing import Any, Dict, List, Optional
import logging
from .plugin import Plugin


class WorkflowStep:
    """Represents a single step in a workflow"""

    def __init__(self, plugin: Plugin, name: str, description: str = ""):
        self.plugin = plugin
        self.name = name
        self.description = description
        self.next_steps: List[WorkflowStep] = []

    async def execute(self, input_data: Any) -> Any:
        """Execute this step and return the result"""
        try:
            result = await self.plugin.execute(input_data)
            return result
        except Exception as e:
            print(f"Error in step {self.name}: {str(e)}")
            raise


class Workflow:
    """Manages the execution of a series of workflow steps"""

    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.first_step: Optional[WorkflowStep] = None

    def add_step(self, step: WorkflowStep) -> "Workflow":
        """Add a step to the workflow"""
        if not self.first_step:
            self.first_step = step
        return self

    async def execute(self, initial_input: Any = None) -> Dict[str, Any]:
        """Execute the entire workflow"""
        if not self.first_step:
            raise ValueError("Workflow has no steps")

        results = {}
        current_step = self.first_step
        current_input = initial_input

        try:
            while current_step:
                step_result = await current_step.execute(current_input)
                results[current_step.name] = step_result

                current_step = (
                    current_step.next_steps[0] if current_step.next_steps else None
                )
                current_input = step_result

        except Exception as e:
            print(f"Workflow error in step {current_step.name}: {str(e)}")
            raise

        return results
