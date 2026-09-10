import pytest

from mylife.mailer import OutboundMessage, SendReceipt, send_then_mark


class GoodMailer:
    def send(self, message):
        return SendReceipt("provider-1")


class FailingMailer:
    def send(self, message):
        raise RuntimeError("temporary provider failure")


def message():
    return OutboundMessage("me@example.com", "Diary", "Write today", "token")


def test_mark_happens_after_success():
    marked = []
    send_then_mark(message(), GoodMailer(), marked.append)
    assert marked == [SendReceipt("provider-1")]


def test_failure_does_not_mark_sent():
    marked = []
    with pytest.raises(RuntimeError):
        send_then_mark(message(), FailingMailer(), marked.append)
    assert marked == []
