from __future__ import annotations

from dataclasses import asdict

from .legacy_mapping import inspect_legacy_mapping
from .migration_plan import build_plan


def migration_report(path):
    mapping = inspect_legacy_mapping(path)
    diaries, images = build_plan(path)
    return {
        "mapping": asdict(mapping),
        "planned_diaries": len(diaries),
        "planned_images": len(images),
        "planned_image_references": sum(len(entry.image_ids) for entry in diaries),
        "ready_for_staging_write": not mapping.unresolved,
    }
