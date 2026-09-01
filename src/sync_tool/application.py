"""Application layer of the program."""

from pathlib import Path
from .sync import find_changed_files
from .state import get_database_connection
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
    from .config import load_config

    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("config/config.json")
    configuration = load_config(config_path)

    
    database_path = Path("data/sync_state.db")

    connection = get_database_connection(database_path)
    try:
        all_changed_files = []

        for directory in configuration.source_directories:
            files_in_directory = scan_directory(directory, configuration.file_types)

            changed_files = find_changed_files(
                connection=connection,
                source_directory=directory,
                files=files_in_directory
            )

            all_changed_files.extend(changed_files)

        print(f"Found {len(all_changed_files)} file(s) needing synchronisation:")
        for file in all_changed_files:
            print(f"  {file.relative_path}  ({file.size} bytes)")
    finally:
        connection.close()