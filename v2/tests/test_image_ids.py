from mylife.image_ids import legacy_image_id


def test_legacy_image_id_is_stable_and_namespaced():
    assert legacy_image_id("Key('UserImage', 1)") == legacy_image_id("Key('UserImage', 1)")
    assert legacy_image_id("Key('UserImage', 1)").startswith("legacy-")
    assert legacy_image_id("Key('UserImage', 1)") != legacy_image_id("Key('UserImage', 2)")
