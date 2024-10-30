from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional
import json
import os
from datetime import datetime
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

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

class WorkflowStep:
    """Represents a single step in a workflow"""
    
    def __init__(self, plugin: Plugin, name: str, description: str = ""):
        self.plugin = plugin
        self.name = name
        self.description = description
        self.next_steps: List[WorkflowStep] = []
    
    async def execute(self, input_data: Any) -> Any:
        """Execute this step and return the result"""
        self.plugin.logger.info(f"Executing step: {self.name}")
        try:
            result = await self.plugin.execute(input_data)
            return result
        except Exception as e:
            self.plugin.logger.error(f"Error in step {self.name}: {str(e)}")
            raise

class Workflow:
    """Manages the execution of a series of workflow steps"""
    
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description
        self.first_step: Optional[WorkflowStep] = None
        self.logger = logging.getLogger(f"pynions.workflow.{name}")
    
    def add_step(self, step: WorkflowStep) -> 'Workflow':
        """Add a step to the workflow"""
        if not self.first_step:
            self.first_step = step
        return self
    
    def connect_steps(self, from_step: WorkflowStep, to_step: WorkflowStep) -> 'Workflow':
        """Connect two steps in the workflow"""
        from_step.next_steps.append(to_step)
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
                self.logger.info(f"Executing workflow step: {current_step.name}")
                step_result = await current_step.execute(current_input)
                results[current_step.name] = step_result
                
                # For now, just take the first next step
                current_step = current_step.next_steps[0] if current_step.next_steps else None
                current_input = step_result
                
        except Exception as e:
            self.logger.error(f"Workflow error in step {current_step.name}: {str(e)}")
            raise
        
        return results

class DataStore:
    """Simple data storage mechanism"""
    
    def __init__(self, storage_dir: str = "data"):
        self.storage_dir = storage_dir
        os.makedirs(storage_dir, exist_ok=True)
        self.logger = logging.getLogger("pynions.datastore")
    
    def save(self, data: Any, name: str) -> str:
        """Save data to storage"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        filepath = os.path.join(self.storage_dir, filename)
        
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.logger.info(f"Data saved to: {filepath}")
        return filepath
    
    def load(self, filepath: str) -> Any:
        """Load data from storage"""
        with open(filepath, 'r') as f:
            return json.load(f)

# Configuration management
class Config:
    """Manages configuration for the framework and plugins"""
    
    def __init__(self, config_path: str = "config.json"):
        self.config_path = config_path
        self.config = self._load_config()
        self.logger = logging.getLogger("pynions.config")
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from file"""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r') as f:
                return json.load(f)
        return {}
    
    def save_config(self):
        """Save configuration to file"""
        with open(self.config_path, 'w') as f:
            json.dump(self.config, f, indent=2)
    
    def get_plugin_config(self, plugin_name: str) -> Dict[str, Any]:
        """Get configuration for a specific plugin"""
        return self.config.get('plugins', {}).get(plugin_name, {})