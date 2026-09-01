from pathlib import Path

from sync_tool.hasher import calculate_sha256


def test_calculate_sha256_is_deterministic(tmp_path: Path):
    file_path = tmp_path / "sample.txt"
    file_path.write_text("hello world")

    first_hash = calculate_sha256(file_path)
    second_hash = calculate_sha256(file_path)

    assert first_hash == second_hash
    assert len(first_hash) == 64  # SHA-256 hex digest length