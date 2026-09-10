#!/usr/bin/env python3
import argparse

from mylife.importer import inspect_backup
from mylife.legacy_mapping import inspect_legacy_mapping
from mylife.migration_plan import build_plan


def main():
    parser = argparse.ArgumentParser(description="Read-only validation of a recovered MyLife backup")
    parser.add_argument("backup")
    args = parser.parse_args()

    summary = inspect_backup(args.backup)
    mapping = inspect_legacy_mapping(args.backup)
    print("Posts            :", summary.posts)
    print("Images           :", summary.images)
    print("Image references :", summary.image_references)
    print("Resolved refs    :", mapping.resolved)
    print("Unresolved refs  :", len(mapping.unresolved))
    if mapping.unresolved:
        raise SystemExit(2)

    diaries, images = build_plan(args.backup)
    planned_refs = sum(len(entry.image_ids) for entry in diaries)
    print("Planned diaries  :", len(diaries))
    print("Planned images   :", len(images))
    print("Planned refs     :", planned_refs)
    if len(diaries) != summary.posts or len(images) != summary.images or planned_refs != summary.image_references:
        raise SystemExit(3)
    print("Migration dry-run: OK")


if __name__ == "__main__":
    main()
