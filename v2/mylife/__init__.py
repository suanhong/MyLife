from flask import Flask, jsonify

from .factory import create_repository
from .settings import Settings
from .web import create_diary_blueprint


def create_app(repository=None) -> Flask:
    app = Flask(__name__)
    settings = Settings.from_env()
    repo = repository or create_repository(settings.project_id)
    app.register_blueprint(create_diary_blueprint(repo))

    @app.get("/healthz")
    def healthz():
        return jsonify(status="ok", service="mylife-v2")

    return app
