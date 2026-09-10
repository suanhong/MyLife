from app.private_images import original_object_name, thumbnail_object_name


def test_image_paths_are_v2_namespaced():
    assert original_object_name("abc") == "v2/images/abc/original"
    assert thumbnail_object_name("abc") == "v2/images/abc/thumbnail"
