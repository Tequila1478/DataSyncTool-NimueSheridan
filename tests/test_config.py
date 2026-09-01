"""Tests for the configuration loading logic of the synchronization tool."""

from pathlib import Path
from sync_tool.config import load_config


def test_load_config_reads_chunk_size(tmp_path: Path):
    """Tests that the load_config function correctly reads the chunk size from the configuration file."""
    config_path = tmp_path / "config.json"

    config_path.write_text(
        """
        {
            "source_directories": [],
            "file_types": [],
            "server_url": "http://localhost:8000",
            "chunk_size": 4194304
        }
        """
    )

    configuration = load_config(config_path)

    assert configuration.chunk_size == 4194304

def test_load_config_normalises_file_types_without_leading_dot(tmp_path: Path):
    """Tests that the load_config function correctly normalises file types without a leading dot."""

    config_path = tmp_path / "config.json"
    config_path.write_text('{"source_directories": [], "file_types": ["txt"], "server_url": "http://localhost"}')

    configuration = load_config(config_path)

    assert configuration.file_types == [".txt"]