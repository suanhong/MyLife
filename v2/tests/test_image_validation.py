import pytest

from mylife.image_validation import validate_image


def test_valid_jpeg_is_accepted():
    validate_image("image/jpeg", b"\xff\xd8\xffdata")


def test_non_image_is_rejected():
    with pytest.raises(ValueError):
        validate_image("application/pdf", b"data")


def test_empty_image_is_rejected():
    with pytest.raises(ValueError):
        validate_image("image/jpeg", b"")


def test_mime_spoof_is_rejected():
    with pytest.raises(ValueError):
        validate_image("image/jpeg", b"not-a-jpeg")
