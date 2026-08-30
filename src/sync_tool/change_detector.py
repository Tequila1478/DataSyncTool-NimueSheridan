from .models import FileState, FileMetadata

def has_changed(current_file: FileMetadata, previous_state: FileState) -> bool:
    """Determines if a file has changed based on its metadata and the last known state."""
    if previous_state is None:
        return True  # No previous state means the file is new or has changed
    if current_file.size != previous_state.size:
        return True  # Size has changed
    if current_file.modified_time != previous_state.modified_time:
        return True  # Modification time has changed
    return False

