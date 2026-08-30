from pathlib import Path

from sync_tool.scanner import scan_directory
from sync_tool.state import initialise_database, save_file_state
from sync_tool.sync import find_changed_files


def test_find_changed_files(tmp_path: Path):
    database_path = tmp_path / "sync_state.db"

    source_directory = tmp_path / "source"
    source_directory.mkdir()

    test_file = source_directory / "test.txt"
    test_file.write_text("This file has changed.")

    initialise_database(database_path)

    files = scan_directory(
        source_directory,
        []
    )

    assert len(files) == 1

    file = files[0]

    save_file_state(
        database_path=database_path,
        source_directory=source_directory,
        relative_path=file.relative_path,
        size=file.size + 1,
        modified_time=file.modified_time,
        sha256="abc123"
    )

    changed_files = find_changed_files(
        database_path=database_path,
        source_directory=source_directory,
        files=files
    )

    assert len(changed_files) == 1
    assert changed_files[0].relative_path == Path("test.txt")