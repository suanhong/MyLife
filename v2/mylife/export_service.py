from __future__ import annotations

from .backup import write_backup


def export_recent(repo, path, limit: int = 365):
    entries = repo.recent(limit)
    return write_backup(path, entries)
