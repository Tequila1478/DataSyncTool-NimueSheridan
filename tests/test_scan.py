"""Tests for the scanner module of the synchronization tool."""

from pathlib import Path
from sync_tool.config import load_config
from sync_tool.scanner import scan_directory


def test_scan_directory_matches_configured_file_types(tmp_path: Path):
    """Tests that the scan_directory function correctly matches files based on the configured file types."""
    source_directory = tmp_path / "source"
    source_directory.mkdir()

    (source_directory / "keep.txt").write_text("kept")
    (source_directory / "skip.md").write_text("skipped")

    config_path = tmp_path / "config.json"
    config_path.write_text(f"""
    {{
        "source_directories": ["{source_directory.as_posix()}"],
        "file_types": [".txt"],
        "server_url": "http://localhost:8000"
    }}
    """)

    configuration = load_config(config_path)

    files = []
    for directory in configuration.source_directories:
        files.extend(scan_directory(directory, configuration.file_types))

    assert len(files) == 1
    assert files[0].relative_path == Path("keep.txt")