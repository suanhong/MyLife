from mylife.image_magic import bytes_match_mime


def test_common_image_signatures():
    assert bytes_match_mime("image/jpeg", b"\xff\xd8\xffx")
    assert bytes_match_mime("image/png", b"\x89PNG\r\n\x1a\nx")
    assert bytes_match_mime("image/gif", b"GIF89ax")
    assert bytes_match_mime("image/webp", b"RIFF0000WEBPx")
    assert not bytes_match_mime("image/jpeg", b"fake")
