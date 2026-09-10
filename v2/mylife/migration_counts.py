EXPECTED_LEGACY_POSTS = 2822
EXPECTED_LEGACY_IMAGES = 252
EXPECTED_LEGACY_IMAGE_REFERENCES = 252


def assert_expected_legacy_counts(posts: int, images: int, refs: int) -> None:
    actual = (posts, images, refs)
    expected = (EXPECTED_LEGACY_POSTS, EXPECTED_LEGACY_IMAGES, EXPECTED_LEGACY_IMAGE_REFERENCES)
    if actual != expected:
        raise ValueError(f"legacy recovery counts changed: expected {expected}, got {actual}")
