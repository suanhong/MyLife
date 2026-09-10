from mylife.internal_auth import scheduler_request_allowed


def test_scheduler_requires_expected_verified_identity():
    assert scheduler_request_allowed({"X-Verified-Service-Account": "scheduler@example"}, "scheduler@example")
    assert not scheduler_request_allowed({}, "scheduler@example")
    assert not scheduler_request_allowed({"X-Verified-Service-Account": "other@example"}, "scheduler@example")
