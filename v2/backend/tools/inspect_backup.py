#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from app.importer import load_diaries_jsonl, load_images_json, summarize_import


def main() -> None:
    parser = argparse.ArgumentParser(description="Inspect a MyLife portable backup directory.")
    parser.add_argument("backup_dir", type=Path)
    args = parser.parse_args()

    backup_dir = args.backup_dir.expanduser().resolve()
    entries = load_diaries_jsonl(backup_dir / "diaries.jsonl")
    images = load_images_json(backup_dir / "images.json", backup_dir / "manifest.json")
    summary = summarize_import(entries, images)

    print("=== MYLIFE V2 BACKUP INSPECTION ===")
    for key, value in summary.items():
        print(f"{key:24s}: {value}")


if __name__ == "__main__":
    main()
