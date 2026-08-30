from dataclasses import dataclass
from pathlib import Path

@dataclass
class FileMetadata:
    """Class to hold metadata for a file."""
    path: Path
    relative_path: Path
    size: int
    modified_time: float

@dataclass
class Configuration:
    """Class to hold configuration for the sync tool."""
    source_directories: list[Path]
    file_types: list[str]
    server_url: str

@dataclass
class FileState:
    """Represents the last successfully synchronised state of a file."""

    size: int
    modified_time: float
    sha256: str