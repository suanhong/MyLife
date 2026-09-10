from mylife.settings import Settings


def test_default_timezone_is_seoul(monkeypatch):
    monkeypatch.delenv("MYLIFE_TIMEZONE", raising=False)
    assert Settings.from_env().timezone == "Asia/Seoul"
