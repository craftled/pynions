import os
import json
import logging
from datetime import datetime
from typing import Any


class DataStore:
    """Manages data persistence for workflow results"""

    def __init__(self, data_dir: str = "data"):
        self.data_dir = data_dir
        os.makedirs(data_dir, exist_ok=True)
        self.logger = logging.getLogger("pynions.datastore")

    def save(self, data: Any, name: str) -> str:
        """Save data to a JSON file with timestamp"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{name}_{timestamp}.json"
        filepath = os.path.join(self.data_dir, filename)

        try:
            with open(filepath, "w") as f:
                json.dump(data, f, indent=2)
            self.logger.info(f"Data saved to {filepath}")
            return filepath
        except Exception as e:
            self.logger.error(f"Error saving data: {str(e)}")
            raise
