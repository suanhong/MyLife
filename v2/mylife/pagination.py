MAX_PAGE_SIZE = 100


def page_size(value: int | None, default: int = 30) -> int:
    size = default if value is None else value
    if size < 1:
        raise ValueError("page size must be positive")
    return min(size, MAX_PAGE_SIZE)
