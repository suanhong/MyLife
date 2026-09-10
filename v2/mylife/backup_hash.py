import hashlib
from pathlib import Path

VERIFIED_LEGACY_BACKUP_SHA256 = "8edb7cfc8bd196d238b0044e146aa0742a01175824c707c4cc673419f01713fb"


def sha256(path: str | Path) -> str:
    digest = hashlib.sha256()
    with Path(path).open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def assert_verified_legacy_backup(path: str | Path) -> None:
    actual = sha256(path)
    if actual.lower() != VERIFIED_LEGACY_BACKUP_SHA256:
        raise ValueError(f"backup SHA-256 mismatch: {actual}")
