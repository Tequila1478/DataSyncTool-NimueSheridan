"""Tests for the synchronization module of the synchronization tool."""

import sqlite3
from pathlib import Path
from sync_tool.hasher import calculate_sha256
from sync_tool.scanner import scan_directory
from sync_tool.state import initialise_database, save_file_state
from sync_tool.sync import find_changed_files


def test_find_changed_files(tmp_path: Path):
    """Tests that the find_changed_files function correctly identifies files that have changed since the last sync."""
    database_path = tmp_path / "sync_state.db"

    source_directory = tmp_path / "source"
    source_directory.mkdir()

    test_file = source_directory / "test.txt"
    test_file.write_text("This file has changed.")

    initialise_database(database_path)

    files = scan_directory(source_directory, [])
    assert len(files) == 1
    file = files[0]

    connection = sqlite3.connect(database_path)
    try:
        save_file_state(
            connection=connection,
            source_directory=source_directory,
            relative_path=file.relative_path,
            size=file.size + 1,
            modified_time=file.modified_time,
            sha256="abc123"
        )

        changed_files = find_changed_files(
            connection=connection,
            source_directory=source_directory,
            files=files
        )
    finally:
        connection.close()

    assert len(changed_files) == 1
    assert changed_files[0].relative_path == Path("test.txt")

def test_file_is_not_flagged_after_state_is_saved(tmp_path: Path):
    """Tests that a file is not flagged as changed after its state has been saved to the database."""
    database_path = tmp_path / "sync_state.db"
    source_directory = tmp_path / "source"
    source_directory.mkdir()

    test_file = source_directory / "test.txt"
    test_file.write_text("Some content")

    initialise_database(database_path)

    files = scan_directory(source_directory, [])
    file = files[0]

    connection = sqlite3.connect(database_path)
    try:
        # First pass: file is new, should be flagged
        first_pass = find_changed_files(
            connection=connection,
            source_directory=source_directory,
            files=files
        )
        assert len(first_pass) == 1

        # Simulate a successful transfer completing
        save_file_state(
            connection=connection,
            source_directory=source_directory,
            relative_path=file.relative_path,
            size=file.size,
            modified_time=file.modified_time,
            sha256=calculate_sha256(file.path)
        )

        # Second pass: same file, unmodified — should now be skipped
        second_pass = find_changed_files(
            connection=connection,
            source_directory=source_directory,
            files=files
        )
        assert len(second_pass) == 0
    finally:
        connection.close()