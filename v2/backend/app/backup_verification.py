from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path

VERIFIED_SHA256 = "8edb7cfc8bd196d238b0044e146aa0742a01175824c707c4cc673419f01713fb"
EXPECTED = {"posts": 2822, "user_images": 252, "image_references": 252}


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def verify_recovered_zip(path: Path) -> dict:
    if sha256(path).lower() != VERIFIED_SHA256:
        raise ValueError("recovered backup SHA-256 does not match verified copy")
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"backup CRC error: {bad}")
        manifest = json.loads(archive.read("manifest.json"))
        counts = manifest.get("counts", {})
        actual = {key: int(counts.get(key, -1)) for key in EXPECTED}
        if actual != EXPECTED:
            raise ValueError(f"recovered backup counts changed: {actual}")
        return manifest
