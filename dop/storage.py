"""Local JSON storage for DOP entries."""

from __future__ import annotations

import json
from pathlib import Path
from tempfile import NamedTemporaryFile

from dop.models import Entry

DATA_FILE = Path(__file__).resolve().parent / "data.json"


class StorageError(Exception):
    """Raised when storage operations fail."""


def ensure_data_file(path: Path = DATA_FILE) -> None:
    """Create data file if it does not already exist."""
    if not path.exists():
        path.write_text("[]\n", encoding="utf-8")


def load_entries(path: Path = DATA_FILE) -> list[Entry]:
    """Load all entries from JSON storage, gracefully recovering from corruption."""
    ensure_data_file(path)
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(payload, list):
            raise StorageError("Invalid data file format: expected a list")
        return [Entry.from_dict(item) for item in payload]
    except json.JSONDecodeError:
        backup = path.with_suffix(".corrupt.json")
        path.replace(backup)
        ensure_data_file(path)
        return []
    except (KeyError, TypeError, ValueError) as err:
        raise StorageError(f"Invalid entry in data file: {err}") from err


def save_entries(entries: list[Entry], path: Path = DATA_FILE) -> None:
    """Safely persist entries to disk using atomic write/replace."""
    ensure_data_file(path)
    serialized = [entry.to_dict() for entry in entries]

    with NamedTemporaryFile("w", delete=False, encoding="utf-8", dir=path.parent) as temp:
        json.dump(serialized, temp, indent=2)
        temp.write("\n")
        temp_path = Path(temp.name)

    temp_path.replace(path)


def add_entry(entry: Entry, path: Path = DATA_FILE) -> None:
    """Append a new entry, enforcing one-entry-per-date."""
    entries = load_entries(path)
    if any(item.date == entry.date for item in entries):
        raise StorageError(f"Entry already exists for date {entry.date}")

    entries.append(entry)
    save_entries(entries, path)


def get_entry_by_date(target_date: str, path: Path = DATA_FILE) -> Entry | None:
    """Return entry for a specific date."""
    entries = load_entries(path)
    for entry in entries:
        if entry.date == target_date:
            return entry
    return None



def remove_entry_by_date(target_date: str, path: Path = DATA_FILE) -> None:
    """Remove entry for a specific date."""
    entries = load_entries(path)
    updated = [entry for entry in entries if entry.date != target_date]
    save_entries(updated, path)
