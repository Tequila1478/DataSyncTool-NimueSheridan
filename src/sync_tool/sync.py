"""Synchronisation logic for the tool."""

import sqlite3
from pathlib import Path
from .change_detector import has_changed
from .hasher import calculate_sha256
from .models import FileMetadata
from .state import get_file_state


def find_changed_files(
    connection: sqlite3.Connection,
    source_directory: Path,
    files: list[FileMetadata]
) -> list[FileMetadata]:
    """Returns files that need to be synchronised."""

    changed_files = []

    for file in files:
        previous_state = get_file_state(
            connection=connection,
            source_directory=source_directory,
            relative_path=file.relative_path
        )

        if not has_changed(current_file=file, previous_state=previous_state):
            continue

        current_hash = calculate_sha256(file.path)

        if previous_state is None or current_hash != previous_state.sha256:
            changed_files.append(file)

    return changed_files