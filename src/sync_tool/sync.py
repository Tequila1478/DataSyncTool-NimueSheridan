from pathlib import Path
from .change_detector import has_changed
from .models import FileMetadata
from .state import get_file_state


def find_changed_files(
    database_path: Path,
    source_directory: Path,
    files: list[FileMetadata]
) -> list[FileMetadata]:
    """Returns files that need to be synchronised."""

    changed_files = []

    for file in files:

        previous_state = get_file_state(
            database_path=database_path,
            source_directory=source_directory,
            relative_path=file.relative_path
        )

        if has_changed(
            current_file=file,
            previous_state=previous_state
        ):
            changed_files.append(file)

    return changed_files