from pathlib import Path

from src.sync_tool.scanner import scan_directory
"""Need to add an actual directory where we want to scan for files. For now, we will use the current directory."""
directory = Path(".")
files = scan_directory(directory)

for file in files:
    print("Path:", file.path)
    print("Size:", file.size)
    print("Modified:", file.modified_time)
    print()