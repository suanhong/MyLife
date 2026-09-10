#!/usr/bin/env python3
"""Extract and import only the exact verified recovery ZIP.

Writes are blocked unless --allow-writes is supplied. Use a v2-only staging
namespace; never point this command at legacy kinds.
"""
from __future__ import annotations

import argparse
import tempfile
import zipfile
from pathlib import Path

from google.cloud import datastore

from app.backup_verification import verify_recovered_zip
from app.importer import load_diaries_jsonl, load_images_json, summarize_import
from app.legacy_mapping import unresolved_image_refs
from app.migration_guard import validate_staging_namespace
from tools.import_backup_to_datastore import diary_entity, image_entity, put_in_batches


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("backup", type=Path)
    parser.add_argument("--project", required=True)
    parser.add_argument("--namespace", required=True)
    parser.add_argument("--batch-size", type=int, default=200)
    parser.add_argument("--allow-writes", action="store_true")
    args = parser.parse_args()

    validate_staging_namespace(args.namespace)
    verify_recovered_zip(args.backup)
    with tempfile.TemporaryDirectory() as temp:
        with zipfile.ZipFile(args.backup) as archive:
            archive.extract("diaries.jsonl", temp)
            archive.extract("images.json", temp)
            archive.extract("manifest.json", temp)
        root = Path(temp)
        entries = load_diaries_jsonl(root / "diaries.jsonl")
        images = load_images_json(root / "images.json", root / "manifest.json")
        summary = summarize_import(entries, images)
        unresolved = unresolved_image_refs(entries, images)
        print(summary)
        print("Unresolved image references:", len(unresolved))
        if unresolved:
            raise SystemExit("Migration blocked: legacy image references are not fully resolved")
        if not args.allow_writes:
            print("Verified dry run only. Re-run with --allow-writes for staging import.")
            return
        client = datastore.Client(project=args.project, namespace=args.namespace)
        put_in_batches(client, [diary_entity(client, entry) for entry in entries], args.batch_size)
        put_in_batches(client, [image_entity(client, image) for image in images], args.batch_size)
        print("Verified staging import complete.")


if __name__ == "__main__":
    main()
