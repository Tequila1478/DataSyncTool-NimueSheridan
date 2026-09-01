"""Tests for the change detection logic of the synchronization tool."""

from pathlib import Path
from sync_tool.change_detector import has_changed
from sync_tool.models import FileMetadata, FileState


def test_new_file_is_changed():
    """Tests that a new file (with no previous state) is considered changed."""
    current_file = FileMetadata(
        path=Path("test.txt"),
        relative_path=Path("test.txt"),
        size=100,
        modified_time=1234567890
    )

    result = has_changed(
        current_file,
        None
    )

    assert result is True


def test_unchanged_file_is_not_changed():
    """Tests that a file with the same size and modified time as its previous state is not considered changed."""
    current_file = FileMetadata(
        path=Path("test.txt"),
        relative_path=Path("test.txt"),
        size=100,
        modified_time=1234567890
    )

    previous_state = FileState(
        size=100,
        modified_time=1234567890,
        sha256="abc123"
    )

    result = has_changed(
        current_file,
        previous_state
    )

    assert result is False


def test_file_with_different_size_is_changed():
    """Tests that a file with a different size than its previous state is considered changed."""
    current_file = FileMetadata(
        path=Path("test.txt"),
        relative_path=Path("test.txt"),
        size=200,
        modified_time=1234567890
    )

    previous_state = FileState(
        size=100,
        modified_time=1234567890,
        sha256="abc123"
    )

    result = has_changed(
        current_file,
        previous_state
    )

    assert result is True


def test_file_with_different_modified_time_is_changed():
    """Tests that a file with a different modified time than its previous state is considered changed."""
    current_file = FileMetadata(
        path=Path("test.txt"),
        relative_path=Path("test.txt"),
        size=100,
        modified_time=9999999999
    )

    previous_state = FileState(
        size=100,
        modified_time=1234567890,
        sha256="abc123"
    )

    result = has_changed(
        current_file,
        previous_state
    )

    assert result is True