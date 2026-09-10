import hashlib


def legacy_image_id(legacy_key: str) -> str:
    return "legacy-" + hashlib.sha256(legacy_key.encode("utf-8")).hexdigest()[:24]
