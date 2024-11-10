from pathlib import Path
from datetime import datetime
from pynions.config import load_config
import re
import json


def slugify(text):
    """Convert text to slug format"""
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "_", text)


def get_valid_status_types():
    """Get list of valid status types from config"""
    config = load_config()
    return list(config["workflow"]["status_types"].keys())


def save_result(content, project_name, status, extension=None):
    """Save content to a project-specific file with timestamp"""
    config = load_config()
    valid_statuses = get_valid_status_types()

    if status not in valid_statuses:
        raise ValueError(
            f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}"
        )

    if extension is None:
        extension = config["workflow"]["status_types"][status]["extensions"][0]

    project_slug = slugify(project_name)
    output_dir = Path(config["storage"]["output_dir"]) / project_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d")
    filename = output_dir / f"{project_slug}_{status}_{timestamp}.{extension}"

    # Handle different content types
    if isinstance(content, (dict, list)):
        with open(filename, "w") as f:
            json.dump(content, f, indent=2)
    else:
        with open(filename, "w") as f:
            f.write(str(content))

    return str(filename)


def save_raw_data(content, source, data_type="scraped_data"):
    """Save raw data with source information"""
    config = load_config()
    raw_dir = Path(config["storage"]["raw_dir"]) / data_type
    raw_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = raw_dir / f"{source}_{timestamp}.txt"

    # Handle different content types
    if isinstance(content, (dict, list)):
        with open(filename, "w") as f:
            json.dump(content, f, indent=2)
    else:
        with open(filename, "w") as f:
            f.write(str(content))

    return str(filename)
