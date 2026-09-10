from __future__ import annotations

from flask import Blueprint, abort, jsonify, request

from .internal_auth import scheduler_request_allowed
from .scheduler import intended_diary_date
from .timezone import seoul_now


def create_scheduler_blueprint(expected_service_account, run_daily):
    bp = Blueprint("scheduler", __name__)

    @bp.post("/internal/daily-mail")
    def daily_mail():
        if not scheduler_request_allowed(request.headers, expected_service_account):
            abort(403)
        day = intended_diary_date(seoul_now())
        receipt = run_daily(day)
        return jsonify(status="already-sent" if receipt is None else "sent")

    return bp
