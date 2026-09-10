from mylife.legacy_refs import reference_aliases


def test_numeric_userimage_key_aliases():
    aliases = reference_aliases("Key('UserImage', 123)")
    assert "123" in aliases
    assert "UserImage:123" in aliases


def test_string_userimage_key_aliases():
    aliases = reference_aliases("Key('UserImage', 'abc')")
    assert "abc" in aliases
    assert "UserImage:abc" in aliases
