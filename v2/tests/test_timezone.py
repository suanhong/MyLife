from mylife.timezone import seoul_now


def test_seoul_now_is_timezone_aware():
    value = seoul_now()
    assert value.tzinfo is not None
    assert getattr(value.tzinfo, "key", None) == "Asia/Seoul"
