from app.retry import retry


def test_retry_after_two_failures():
    calls = []
    def op():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("temporary")
        return "ok"
    assert retry(op, attempts=3, base_delay=0, sleep=lambda _: None) == "ok"
