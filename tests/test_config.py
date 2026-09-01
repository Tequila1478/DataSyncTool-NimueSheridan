from pathlib import Path

from sync_tool.config import load_config


def test_load_config_reads_chunk_size(tmp_path: Path):

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