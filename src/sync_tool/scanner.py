from pathlib import Path

from .models import FileMetadata

def scan_directory(directory: Path):
    """Scans the given directory and returns a list of all files in it."""
    files = []

    for path in directory.rglob("*"):
        if path.is_file():
            file_info = path.stat()

            metadata = FileMetadata(
                path=path,
                size=file_info.st_size,
                modified_time=file_info.st_mtime
            )
            files.append(metadata)

    return files