from mylife.retry import retry


def test_retry_succeeds_after_transient_failures():
    calls = []
    def operation():
        calls.append(1)
        if len(calls) < 3:
            raise RuntimeError("temporary")
        return "ok"
    assert retry(operation, attempts=3, base_delay=0, sleep=lambda _: None) == "ok"
    assert len(calls) == 3
