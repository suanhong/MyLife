from app.scheduler_auth import scheduler_allowed


def test_scheduler_identity_must_match():
    assert scheduler_allowed("scheduler@example", "scheduler@example")
    assert not scheduler_allowed("other@example", "scheduler@example")
