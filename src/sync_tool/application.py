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