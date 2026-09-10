import pytest

from app.mail_config import MailConfig


def test_gmail_config():
    MailConfig("gmail", "me@example.com").validate()


def test_unknown_provider_rejected():
    with pytest.raises(ValueError):
        MailConfig("unknown", "me@example.com").validate()
