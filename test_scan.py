from pathlib import Path

from src.sync_tool.scanner import scan_directory

directory = Path(".")
files = scan_directory(directory)

for file in files:
    print(file)