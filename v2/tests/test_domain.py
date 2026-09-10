from datetime import date

from mylife.domain import should_send_daily_prompt


def test_prompt_is_sent_once_on_requested_local_date():
    today = date(2026, 9, 10)
    assert should_send_daily_prompt(already_sent=False, local_date=today, requested_date=today)
    assert not should_send_daily_prompt(already_sent=True, local_date=today, requested_date=today)


def test_prompt_is_not_sent_for_wrong_local_date():
    assert not should_send_daily_prompt(
        already_sent=False,
        local_date=date(2026, 9, 11),
        requested_date=date(2026, 9, 10),
    )
