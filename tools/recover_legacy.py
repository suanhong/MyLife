#!/usr/bin/env python3
"""Read-only recovery utility for legacy MyLife data on Google Cloud.

Runs outside the Python 2 App Engine application (for example in Cloud Shell).
It never writes to Datastore or Cloud Storage. It exports Post/UserImage data,
downloads original images with retries/resume, hashes recovered files, and
builds a disk-backed portable ZIP.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import time
import zipfile
from datetime import date, datetime
from pathlib import Path

from google.api_core.exceptions import DeadlineExceeded, RetryError
from google.cloud import datastore, storage


def scalar(value):
    if isinstance(value, (datetime, date)):
        return value.isoformat()
    if isinstance(value, bytes):
        return value.decode("utf-8", errors="replace")
    if isinstance(value, list):
        return [scalar(v) for v in value]
    if value is None or isinstance(value, (str, int, float, bool)):
        return value
    return str(value)


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def fetch_kind(client, kind: str, page_size: int, retries: int):
    cursor = None
    while True:
        for attempt in range(1, retries + 1):
            try:
                query = client.query(kind=kind)
                iterator = query.fetch(limit=page_size, start_cursor=cursor, timeout=300)
                page = next(iterator.pages)
                batch = list(page)
                next_cursor = iterator.next_page_token
                break
            except (DeadlineExceeded, RetryError):
                if attempt == retries:
                    raise
                print(f"{kind}: timeout, retry {attempt}/{retries}", flush=True)
                time.sleep(attempt * 3)
        for entity in batch:
            yield entity
        if not next_cursor:
            return
        cursor = next_cursor


def post_date(entity) -> str:
    value = entity.get("date")
    if isinstance(value, datetime):
        return value.date().isoformat()
    if isinstance(value, date):
        return value.isoformat()
    return str(value) if value else "unknown"


def export_posts(ds, root: Path, page_size: int, retries: int):
    diary_dir = root / "diaries"
    diary_dir.mkdir(parents=True, exist_ok=True)
    jsonl = root / "diaries.jsonl"
    count = 0
    refs = []
    with jsonl.open("w", encoding="utf-8") as out:
        for post in fetch_kind(ds, "Post", page_size, retries):
            count += 1
            text = post.get("text", "")
            if isinstance(text, bytes):
                text = text.decode("utf-8", errors="replace")
            images = scalar(post.get("images", [])) or []
            refs.extend(images)
            item = {
                "key": str(post.key), "date": post_date(post), "text": text,
                "source": scalar(post.get("source")), "created": scalar(post.get("created")),
                "updated": scalar(post.get("updated")), "has_images": scalar(post.get("has_images")),
                "images": images,
            }
            out.write(json.dumps(item, ensure_ascii=False) + "\n")
            filename = f"{count:06d}_{item['date']}.md"
            (diary_dir / filename).write_text(f"# {item['date']}\n\n{text or ''}\n", encoding="utf-8")
            if count % 200 == 0:
                print(f"Posts recovered: {count}", flush=True)
    return count, refs


def export_images(ds, gcs, bucket_name: str, root: Path, page_size: int, retries: int):
    photo_dir = root / "photos"
    photo_dir.mkdir(parents=True, exist_ok=True)
    bucket = gcs.bucket(bucket_name)
    metadata = []
    manifest = []
    for index, image in enumerate(fetch_kind(ds, "UserImage", page_size, retries), 1):
        item = {"key": str(image.key)}
        item.update({key: scalar(value) for key, value in image.items()})
        metadata.append(item)
        filename = image.get("filename")
        object_key = image.get("original_size_key")
        if not filename or not object_key:
            raise RuntimeError(f"UserImage {image.key} lacks filename/original_size_key")
        target = photo_dir / filename
        blob = bucket.blob(object_key)
        expected_size = blob.size
        if expected_size is None:
            blob.reload(timeout=300)
            expected_size = blob.size
        complete = target.exists() and (expected_size is None or target.stat().st_size == expected_size)
        if not complete:
            for attempt in range(1, retries + 1):
                try:
                    blob.download_to_filename(str(target), timeout=300)
                    break
                except Exception:
                    if attempt == retries:
                        raise
                    print(f"Image {index}: retry {attempt}/{retries}", flush=True)
                    time.sleep(attempt * 3)
        manifest.append({"filename": filename, "gcs_key": object_key,
                         "bytes": target.stat().st_size, "sha256": sha256_file(target)})
        if index % 25 == 0:
            print(f"Images recovered: {index}", flush=True)
    (root / "images.json").write_text(json.dumps(metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return metadata, manifest


def build_backup(root: Path, zip_path: Path, post_count: int, refs, images, photo_manifest):
    manifest = {
        "format": "MyLife portable recovery backup", "version": 1,
        "counts": {"posts": post_count, "user_images": len(images),
                   "photo_files": len(photo_manifest), "image_references": len(refs),
                   "unique_image_references": len(set(refs))},
        "photos": photo_manifest,
    }
    (root / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
        for name in ("diaries.jsonl", "images.json", "manifest.json"):
            archive.write(root / name, arcname=name)
        for directory in ("diaries", "photos"):
            for path in sorted((root / directory).iterdir()):
                if path.is_file():
                    archive.write(path, arcname=f"{directory}/{path.name}")
    with zipfile.ZipFile(zip_path, "r") as archive:
        bad = archive.testzip()
        if bad:
            raise RuntimeError(f"ZIP CRC verification failed: {bad}")
    return sha256_file(zip_path)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--project", required=True)
    parser.add_argument("--bucket", required=True)
    parser.add_argument("--output", default="mylife-recovery")
    parser.add_argument("--zip", dest="zip_name", default="mylife-backup.zip")
    parser.add_argument("--page-size", type=int, default=200)
    parser.add_argument("--retries", type=int, default=5)
    args = parser.parse_args()
    root = Path(args.output).expanduser().resolve()
    root.mkdir(parents=True, exist_ok=True)
    ds = datastore.Client(project=args.project)
    gcs = storage.Client(project=args.project)
    print("Read-only recovery: no cloud writes will be performed.")
    post_count, refs = export_posts(ds, root, args.page_size, args.retries)
    images, photos = export_images(ds, gcs, args.bucket, root, min(args.page_size, 50), args.retries)
    digest = build_backup(root, Path(args.zip_name).expanduser().resolve(), post_count, refs, images, photos)
    print(f"Posts: {post_count}; Images: {len(images)}; Refs: {len(refs)}")
    print(f"ZIP SHA256: {digest}")


if __name__ == "__main__":
    main()
