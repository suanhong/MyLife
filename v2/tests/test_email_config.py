import pytest

from mylife.email_config import EmailConfig


def test_gmail_config_is_valid():
    EmailConfig("gmail", "me@example.com").validate()


def test_unknown_provider_is_rejected():
    with pytest.raises(ValueError):
        EmailConfig("unknown", "me@example.com").validate()
