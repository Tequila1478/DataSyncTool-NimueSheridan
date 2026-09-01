from pathlib import Path

from .models import Configuration, FileMetadata
from .scanner import scan_directory


def scan_configured_directories(
    configuration: Configuration
) -> list[FileMetadata]:
    """Scans all directories specified in the configuration."""

    files = []

    for directory in configuration.source_directories:

        directory_files = scan_directory(
            directory,
            configuration.file_types
        )

        files.extend(directory_files)

    return files

if __name__ == "__main__":
    import sys
    from pathlib import Path
    from .config import load_config

    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("config/config.json")
    configuration = load_config(config_path)

    files = scan_configured_directories(configuration)

    print(f"Found {len(files)} file(s) matching configuration:")
    for file in files:
        print(f"  {file.relative_path}  ({file.size} bytes)")