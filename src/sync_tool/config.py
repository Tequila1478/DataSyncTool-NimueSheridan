import json
from pathlib import Path

from .models import Configuration

def load_config(config_path: Path) -> Configuration:
    """Loads the configuration from a JSON file."""
    with open(config_path, "r") as file:
        config_data = json.load(file)

    directories = []

    for directory in config_data.get("source_directories", []):
        path = Path(directory)

        if not path.exists():
            raise ValueError(f"Directory does not exist: {path}")

        if not path.is_dir():
            raise ValueError(f"Path is not a directory: {path}")

        directories.append(path)

    file_types = []

    for file_type in config_data.get("file_types", []):
        file_types.append(file_type.lower())

    server_url = config_data.get("server_url", "")
    
    return Configuration(source_directories=directories, file_types=file_types, server_url=server_url)

    