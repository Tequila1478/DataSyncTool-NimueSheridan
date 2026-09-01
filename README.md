# DataSyncTool-NimueSheridan
Python prototype for reliable, bandwidth-efficient file synchronisation showcasing the core requirements of detecting file changes.

# Rationale
The reason I chose to focus on detecting file changes is because I believe it to be the underlying backbone of this tool. When designed and implemented correctly, proper change detection with intelligent determination of changed files contributes to more than a single key requirement: 
- It is the mechanism that the monitoring of directories will sit upon;  
- it supports reduced bandwidth by being the foundation of minimising what actually needs to be transferred; 
- builds the basis upon which the integrity and file verification sits (SHA-256 hash recording);
- and it supports future delta sync incorporation. 

It was also a relatively simple part of the project to implement while still showcasing several moving pieces with easily separable, well-tested logic that demonstrates clean architecture and good coding practices.

# Current Implementation
Directory scanning (independent of watcher), configuration loading (independent of GUI), Metadata Tracking, SHA-256 Hashing and local synchronisation state

Every run currently reports all matching files as needing sync, since state is only persisted after a real transfer completes, which isn't implemented yet. This is intentional, not a bug, see the Reliability section in the design document. To see how the unchanged -> Skipped pipeline works please see `test_file_is_not_flagged_after_state_is_saved`. I did not want to implement saving the state as sync as this should be confirmed by the server side once the transfer is completed.

# How to Run
1. Create and activate a virtual environment:
```python
python -m venv .venv
.venv\Scripts\activate # Windows
source .venv/bin/activate # macOS/Linux
```
2. Install the project in editable mode:
pip install -e
3. Edit `config/config.json` to point at the directories you want to scan, e.g.:
```json
   {
       "source_directories": ["C:/example/folder"],
       "file_types": [".txt", ".pdf", ".docx"],
       "server_url": "https://sync-server.example",
       "chunk_size": 8388608
   }
```
4. Run the Scanner
```pyton
python -m sync_tool.application
```
This scans the configured directories and lists the files found. Change detection, hashing, and upload are not yet wired into this entrypoint — see `sync.py` for the current change-detection logic, which is exercised directly by the test suite for now.

# How to use tests
1. Install the project with its test dependencies:
```python
pip install -e".[dev]"
```
(This installs `pytest` alongside the project. If you haven't added the `dev` optional-dependency group to `pyproject.toml` yet, run `pip install -e . pytest` instead.)
2. Run the full test suite from the repository root:
```python
pytest
```
or, for more details on each test:
```python
pytest -v
```
All tests use `tmp_path`, a built-in pytest fixture that creates a temporary directory for each test — so running the suite is safe and won't touch your real config, database, or source directories.
# Planned
Server API, chuncked upload/resumability, retry manager, GUI