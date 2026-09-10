import pytest

from app.mail_send_state import send_then_mark


class Good:
    def send(self, message): return "receipt"


class Bad:
    def send(self, message): raise RuntimeError("temporary")


def test_success_marks_after_send():
    marked = []
    assert send_then_mark("message", Good(), marked.append) == "receipt"
    assert marked == ["receipt"]


def test_failure_does_not_mark():
    marked = []
    with pytest.raises(RuntimeError):
        send_then_mark("message", Bad(), marked.append)
    assert marked == []
