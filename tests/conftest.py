from __future__ import annotations

import pytest
from flask import Flask
from flask.testing import FlaskClient

from flask_orjson import OrjsonProvider


@pytest.fixture
def app() -> Flask:
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "secret_key"
    app.json = OrjsonProvider(app)
    return app


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    return app.test_client()
