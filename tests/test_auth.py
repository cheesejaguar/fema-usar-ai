import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from flask import Flask
from utils.auth import require_api_key


def create_app(api_key="secret"):
    app = Flask(__name__)
    app.config["API_KEY"] = api_key

    @app.route("/protected")
    @require_api_key
    def protected():
        return "ok"

    return app


def test_require_api_key_success():
    app = create_app()
    client = app.test_client()
    resp = client.get("/protected", headers={"X-API-Key": "secret"})
    assert resp.status_code == 200
    assert resp.data == b"ok"


def test_require_api_key_failure():
    app = create_app()
    client = app.test_client()
    resp = client.get("/protected")
    assert resp.status_code == 401
    assert resp.get_json()["error"] == "Unauthorized"
