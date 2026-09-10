from mylife.thumbnail import thumbnail_object_name


def test_thumbnail_object_path_is_private_namespace():
    assert thumbnail_object_name("abc") == "v2/images/abc/thumbnail"
