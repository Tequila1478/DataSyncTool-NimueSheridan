from pathlib import Path
import hashlib

def calculate_sha256(file_path: Path) -> str:
    """Calculates the SHA-256 hash of a file."""
    sha256 = hashlib.sha256()

    with open(file_path, "rb") as file:
        while True:
            # Read the file in chunks to avoid using too much memory
            data = file.read(1024 * 1024)  # Read in 1MB chunks
            if not data:
                break
            sha256.update(data)

    return sha256.hexdigest()