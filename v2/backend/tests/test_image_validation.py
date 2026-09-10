import pytest

from app.image_validation import validate_image


def test_valid_jpeg():
    validate_image("image/jpeg", b"\xff\xd8\xffdata")


def test_spoofed_jpeg_rejected():
    with pytest.raises(ValueError):
        validate_image("image/jpeg", b"not-jpeg")
