from pathlib import Path

from src.sync_tool.state import (
    initialise_database,
    get_file_state,
    save_file_state
)


database_path = Path("data/sync_state.db")

database_path.parent.mkdir(exist_ok=True)

initialise_database(database_path)


source_directory = Path("C:/Users/Nimue/Documents/DataSyncTest")
relative_path = Path("test.txt")


state = get_file_state(
    database_path,
    source_directory,
    relative_path
)

print("Before saving:")
if state is None:
    print("No previous state found.")
else:
    print("Size:", state.size)
    print("Modified:", state.modified_time)
    print("SHA-256:", state.sha256)


save_file_state(
    database_path=database_path,
    source_directory=source_directory,
    relative_path=relative_path,
    size=200,
    modified_time=9999999999,
    sha256="sdgsd123"
)


state = get_file_state(
    database_path,
    source_directory,
    relative_path
)

print("After saving:")
if state is None:
    print("No current state found.")
else:
    print("Size:", state.size)
    print("Modified:", state.modified_time)
    print("SHA-256:", state.sha256)