from flask import Flask

from mylife.scheduler_route import create_scheduler_blueprint


def test_scheduler_route_requires_verified_identity():
    app = Flask(__name__)
    app.register_blueprint(create_scheduler_blueprint("scheduler@example", lambda day: None))
    assert app.test_client().post("/internal/daily-mail").status_code == 403
