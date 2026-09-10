from types import SimpleNamespace

from app.legacy_mapping import unresolved_image_refs


def test_legacy_key_reference_resolves():
    entry = SimpleNamespace(image_refs=["Key('UserImage', 1)"])
    image = SimpleNamespace(legacy_key="Key('UserImage', 1)", filename="photo.jpg", storage_key="photo.jpg")
    assert unresolved_image_refs([entry], [image]) == []
