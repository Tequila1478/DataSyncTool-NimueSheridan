import sqlite3
from pathlib import Path

from sync_tool.state import initialise_database, get_file_state, save_file_state


def test_save_and_retrieve_file_state(tmp_path: Path):
    database_path = tmp_path / "sync_state.db"
    source_directory = tmp_path / "source"
    relative_path = Path("test.txt")

    initialise_database(database_path)

    connection = sqlite3.connect(database_path)
    try:
        assert get_file_state(connection, source_directory, relative_path) is None

        save_file_state(
            connection=connection,
            source_directory=source_directory,
            relative_path=relative_path,
            size=200,
            modified_time=9999999999,
            sha256="abc123"
        )

        state = get_file_state(connection, source_directory, relative_path)
        assert state is not None
        assert state.size == 200
        assert state.sha256 == "abc123"
    finally:
        connection.close()