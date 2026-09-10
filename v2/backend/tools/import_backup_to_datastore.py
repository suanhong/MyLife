#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from google.cloud import datastore

from app.importer import load_diaries_jsonl, load_images_json, summarize_import

DIARY_KIND = "DiaryEntryV2"
IMAGE_KIND = "ImageRefV2"


def put_in_batches(client: datastore.Client, entities: list[datastore.Entity], batch_size: int) -> None:
    for start in range(0, len(entities), batch_size):
        batch = entities[start : start + batch_size]
        client.put_multi(batch)
        print(f"Imported {start + len(batch)} / {len(entities)}", flush=True)


def diary_entity(client: datastore.Client, entry) -> datastore.Entity:
    entity = datastore.Entity(
        key=client.key(DIARY_KIND, entry.id),
        exclude_from_indexes=("text", "metadata"),
    )
    entity.update(
        {
            "id": entry.id,
            "entry_date": entry.entry_date.isoformat(),
            "text": entry.text,
            "source": entry.source,
            "created_at": entry.created_at.isoformat() if entry.created_at else None,
            "updated_at": entry.updated_at.isoformat() if entry.updated_at else None,
            "image_refs": entry.image_refs,
            "legacy_key": entry.legacy_key,
            "metadata": entry.metadata,
        }
    )
    return entity


def image_entity(client: datastore.Client, image) -> datastore.Entity:
    entity_id = image.legacy_key or image.filename
    entity = datastore.Entity(key=client.key(IMAGE_KIND, entity_id))
    entity.update(
        {
            "legacy_key": image.legacy_key,
            "filename": image.filename,
            "original_filename": image.original_filename,
            "content_type": image.content_type,
            "size_bytes": image.size_bytes,
            "sha256": image.sha256,
            "storage_key": image.storage_key,
            "created_at": image.created_at.isoformat() if image.created_at else None,
        }
    )
    return entity


def main() -> None:
    parser = argparse.ArgumentParser(description="Import a recovered MyLife backup into Datastore v2 kinds.")
    parser.add_argument("backup_dir", type=Path)
    parser.add_argument("--project", required=True)
    parser.add_argument("--namespace", default=None)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--batch-size", type=int, default=200)
    args = parser.parse_args()

    backup_dir = args.backup_dir.expanduser().resolve()
    entries = load_diaries_jsonl(backup_dir / "diaries.jsonl")
    images = load_images_json(backup_dir / "images.json", backup_dir / "manifest.json")
    summary = summarize_import(entries, images)

    print("=== MYLIFE V2 DATASTORE IMPORT ===")
    for key, value in summary.items():
        print(f"{key:24s}: {value}")

    if args.dry_run:
        print("Dry run only. No Datastore writes performed.")
        return

    client = datastore.Client(project=args.project, namespace=args.namespace)
    diary_entities = [diary_entity(client, entry) for entry in entries]
    image_entities = [image_entity(client, image) for image in images]

    print("Importing diary entries...")
    put_in_batches(client, diary_entities, args.batch_size)
    print("Importing image metadata...")
    put_in_batches(client, image_entities, args.batch_size)
    print("Import complete.")


if __name__ == "__main__":
    main()
