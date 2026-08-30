from pathlib import Path

def scan_directory(directory: Path):
    """Scans the given directory and returns a list of all files in it."""
    files = []

    for path in directory.rglob("*"):
        if path.is_file():
            files.append(path)

    return files