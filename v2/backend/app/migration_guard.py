LEGACY_OR_EMPTY_NAMESPACES = {"", "legacy", "default", None}


def validate_staging_namespace(namespace: str | None) -> str:
    if namespace in LEGACY_OR_EMPTY_NAMESPACES:
        raise ValueError("a dedicated v2 staging namespace is required")
    if not namespace.startswith("mylife-v2-"):
        raise ValueError("staging namespace must start with mylife-v2-")
    return namespace
