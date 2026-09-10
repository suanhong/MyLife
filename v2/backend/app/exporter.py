from __future__ import annotations

import hashlib
import json
import zipfile
from pathlib import Path


def write_entries_zip(path: Path, entries) -> str:
    """Write export directly to disk; never hold the whole ZIP in memory."""
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, allowZip64=True) as archive:
        lines = []
        for entry in entries:
            payload = entry.model_dump(mode="json") if hasattr(entry, "model_dump") else dict(entry)
            lines.append(json.dumps(payload, ensure_ascii=False))
        archive.writestr("diaries.jsonl", "\n".join(lines) + ("\n" if lines else ""))
        archive.writestr("manifest.json", json.dumps({"posts": len(lines)}))
    with zipfile.ZipFile(path) as archive:
        bad = archive.testzip()
        if bad:
            raise ValueError(f"export CRC error: {bad}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()
