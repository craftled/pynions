"""Utility functions for Pynions"""

from pathlib import Path
from datetime import datetime
from pynions.core.config import config
import re
import json


def slugify(text):
    """Convert text to slug format"""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "_", text)


def get_valid_status_types():
    """Get list of valid status types from config"""
    # This function is no longer needed with the new simplified config
    pass


def save_result(content, project_name, status, extension=None, filename_prefix=None):
    """Save content to a project-specific file with timestamp"""
    # Get output folder from config
    output_folder = config.get("output_folder", "data")
    
    # Create output directory if it doesn't exist
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    prefix = f"{filename_prefix}_" if filename_prefix else ""
    filename = f"{prefix}{timestamp}.txt"
    
    # Save the content
    filepath = output_path / filename
    with open(filepath, "w") as f:
        if isinstance(content, (dict, list)):
            json.dump(content, f, indent=2)
        else:
            f.write(str(content))
            
    return str(filepath)


def save_raw_data(content, source, data_type="scraped_data"):
    """Save raw data with source information"""
    # Get output folder from config
    output_folder = config.get("output_folder", "data")
    
    # Create output directory if it doesn't exist
    output_path = Path(output_folder)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{source}_{timestamp}.txt"
    
    # Save the content
    filepath = output_path / filename
    with open(filepath, "w") as f:
        if isinstance(content, (dict, list)):
            json.dump(content, f, indent=2)
        else:
            f.write(str(content))
            
    return str(filepath)
