from pathlib import Path

from sync_tool.hasher import calculate_sha256

file_path = Path("config/config.json")

file_hash = calculate_sha256(file_path)

print(f"SHA-256 hash of {file_path}: {file_hash}")