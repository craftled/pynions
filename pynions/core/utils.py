from pathlib import Path
from datetime import datetime
from pynions.config import load_config
import re


def slugify(text):
    """Convert text to slug format"""
    # Convert to lowercase and replace spaces with underscores
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "_", text)


def get_valid_status_types():
    """Get list of valid status types from config"""
    config = load_config()
    return list(config["workflow"]["status_types"].keys())


def save_result(content, project_name, status, extension=None):
    """
    Save content to a project-specific file with timestamp

    Args:
        content: Content to save
        project_name: Name of the project/topic
        status: Status of the content (must be one of the configured status types)
        extension: Optional file extension (if None, uses default from config)
    """
    config = load_config()
    valid_statuses = get_valid_status_types()

    if status not in valid_statuses:
        raise ValueError(
            f"Invalid status: {status}. Must be one of: {', '.join(valid_statuses)}"
        )

    # Get default extension for this status if none provided
    if extension is None:
        extension = config["workflow"]["status_types"][status]["extensions"][0]

    # Create slug from project name
    project_slug = slugify(project_name)

    # Create project directory in output
    output_dir = Path(config["storage"]["output_dir"]) / project_slug
    output_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with project, status and date
    timestamp = datetime.now().strftime("%Y%m%d")
    filename = output_dir / f"{project_slug}_{status}_{timestamp}.{extension}"

    # Save content
    with open(filename, "w") as f:
        f.write(content)

    return str(filename)


def save_raw_data(content, source, data_type="scraped_data"):
    """
    Save raw data with source information

    Args:
        content: Raw content to save
        source: Source of the data (e.g., 'serper', 'playwright')
        data_type: Type of raw data (scraped_data, logs, etc.)
    """
    config = load_config()
    raw_dir = Path(config["storage"]["raw_dir"]) / data_type

    # Create raw directory if it doesn't exist
    raw_dir.mkdir(parents=True, exist_ok=True)

    # Generate filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = raw_dir / f"{source}_{timestamp}.txt"

    # Save content
    with open(filename, "w") as f:
        f.write(content)

    return str(filename)
