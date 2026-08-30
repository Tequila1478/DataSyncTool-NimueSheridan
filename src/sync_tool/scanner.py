from pathlib import Path

from .models import FileMetadata

def scan_directory(directory: Path, file_types: list[str]):
    """Scans the given directory and returns a list of all metadata in it that match the specified file types."""
    files = []

    for path in directory.rglob("*"):
        if path.is_file():
            if file_types and path.suffix.lower() not in file_types:
                continue

            file_info = path.stat()

            metadata = FileMetadata(
                path=path,
                size=file_info.st_size,
                modified_time=file_info.st_mtime
            )
            files.append(metadata)

    return files