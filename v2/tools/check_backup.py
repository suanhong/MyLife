#!/usr/bin/env python3
import argparse

from mylife.importer import inspect_backup
from mylife.legacy_mapping import inspect_legacy_mapping


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


if __name__ == "__main__":
    main()
