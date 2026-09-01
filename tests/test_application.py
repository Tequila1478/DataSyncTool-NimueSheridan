"""Tests for the application layer of the synchronization tool."""

from pathlib import Path
from sync_tool.application import scan_configured_directories
from sync_tool.models import Configuration


def test_scan_configured_directories(tmp_path: Path):
    """Tests that the scan_configured_directories function correctly scans directories and retrieves file metadata."""

    source_directory = tmp_path / "source"
    source_directory.mkdir()

    first_file = source_directory / "first.txt"
    first_file.write_text("First file")

    second_file = source_directory / "second.txt"
    second_file.write_text("Second file")

    configuration = Configuration(
        source_directories=[source_directory],
        file_types=[],
        server_url="http://localhost"
    )

    files = scan_configured_directories(configuration)

    assert len(files) == 2

    relative_paths = {
        file.relative_path
        for file in files
    }

    assert relative_paths == {
        Path("first.txt"),
        Path("second.txt")
    }