from __future__ import annotations

from google.cloud import datastore

from .datastore_repository import DatastoreDiaryRepository
from .repository import MemoryDiaryRepository


def create_repository(project_id: str | None = None):
    """Use Datastore when a project is configured; otherwise support local tests/dev."""
    if project_id:
        return DatastoreDiaryRepository(datastore.Client(project=project_id))
    return MemoryDiaryRepository()
