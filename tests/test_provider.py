from __future__ import annotations

import typing as t
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from decimal import Decimal

import orjson
import pytest
from flask import Flask
from flask import request
from flask.testing import FlaskClient

from flask_orjson import OrjsonProvider


def test_request_response(app: Flask, client: FlaskClient) -> None:
    @app.post("/")
    def echo() -> t.Any:
        return request.json

    class User:
        def __init__(self, name: str) -> None:
            self.name = name

        def __html__(self) -> str:
            return f"<a>{self.name}</a>"

    pst = timezone(timedelta(hours=-8), "PST")
    rv = client.post(
        "/",
        json={
            "str": "v",
            "int": 1,
            "float": 2.0,
            "datetime-naive": datetime(2024, 1, 12, 9, 42),
            "datetime-aware": datetime(2024, 1, 12, 9, 42, tzinfo=pst),
            "decimal": Decimal("3.14159"),
            "html": User("flask"),
        },
    )
    assert rv.json == {
        "str": "v",
        "int": 1,
        "float": 2.0,
        "datetime-naive": "2024-01-12T09:42:00+00:00",
        "datetime-aware": "2024-01-12T09:42:00-08:00",
        "decimal": "3.14159",
        "html": "<a>flask</a>",
    }


def test_instance_option(app: Flask) -> None:
    provider = t.cast(OrjsonProvider, app.json)
    provider.option = orjson.OPT_NON_STR_KEYS
    rv = app.json.dumps({1: "i"})
    assert rv == """{"1":"i"}"""


def test_method_option(app: Flask) -> None:
    rv = app.json.dumps({1: "i"}, option=orjson.OPT_NON_STR_KEYS)
    assert rv == """{"1":"i"}"""


def test_default_unsupported(app: Flask) -> None:
    with pytest.raises(TypeError):
        app.json.dumps({"a": ...})


def test_instance_default(app: Flask) -> None:
    def default(o: t.Any) -> t.Any:
        return "default"

    provider = t.cast(OrjsonProvider, app.json)
    provider.default = default
    rv = app.json.dumps({"a": Decimal(1)})
    assert rv == """{"a":"default"}"""


def test_method_default(app: Flask) -> None:
    def default(o: t.Any) -> t.Any:
        return "default"

    rv = app.json.dumps({"a": Decimal(1)}, default=default)
    assert rv == """{"a":"default"}"""
