from pathlib import Path
from src.sync_tool.config import load_config
from src.sync_tool.scanner import scan_directory

config_path = Path("config/config.json")

configuration = load_config(config_path)

for directory in configuration.source_directories:

    print("Scanning:", directory)

    files = scan_directory(
        directory,
        configuration.file_types
    )

    for file in files:
        print("Path:", file.path)
        print("Relative Path:", file.relative_path)
        print("Size:", file.size)
        print("Modified:", file.modified_time)
        print()