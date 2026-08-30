import sqlite3
from pathlib import Path
from .models import FileState

def initialise_database(db_path: Path) -> None:
    """Initializes the SQLite database with the required tables."""
    connection = sqlite3.connect(db_path)
    cursor = connection.cursor()

    # Create a table for file metadata
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS files (
            source_directory TEXT NOT NULL,
            relative_path TEXT NOT NULL,
            size INTEGER NOT NULL,
            modified_time REAL NOT NULL,
            sha256 TEXT NOT NULL,

            PRIMARY KEY (source_directory, relative_path)
        )
    ''')

    connection.commit()
    connection.close()

def get_file_state(
        database_path: Path,
        source_directory: Path,
        relative_path: Path
) ->FileState | None:
    """Retrieves the state of a file from the database."""
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        SELECT size, modified_time, sha256
        FROM files
        WHERE source_directory = ? AND relative_path = ?
    ''', (str(source_directory), str(relative_path)))

    result = cursor.fetchone()
    connection.close()

    if result is None:
        return None

    return FileState(
        size=result[0],
        modified_time=result[1],
        sha256=result[2]
    )

def save_file_state(
        database_path: Path,
        source_directory: Path,
        relative_path: Path,
        size: int,
        modified_time: float,
        sha256: str
):
    """Stores the state of a successfully synchronised file."""
    connection = sqlite3.connect(database_path)
    cursor = connection.cursor()

    cursor.execute('''
        INSERT INTO files (
            source_directory, 
            relative_path, 
            size, 
            modified_time, 
            sha256)
        VALUES (?, ?, ?, ?, ?)
        ON CONFLICT(source_directory, relative_path)
    DO UPDATE SET
        size = excluded.size,
        modified_time = excluded.modified_time,
        sha256 = excluded.sha256
    ''', (str(source_directory), str(relative_path), size, modified_time, sha256))

    connection.commit()
    connection.close()