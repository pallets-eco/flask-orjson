# flask-orjson

[![PyPI version](https://badge.fury.io/py/flask-orjson.svg)](https://badge.fury.io/py/flask-orjson)
[![License](https://img.shields.io/badge/license-LGPL_v2-red.svg)](https://raw.githubusercontent.com/CheeseCake87/flask-orjson/master/LICENSE)

`pip install flask-orjson`

Flask with orjson.

[https://github.com/ijl/orjson](https://github.com/ijl/orjson)

```python
from dataclasses import dataclass
from datetime import datetime

from flask import Flask, request

from flask_orjson import ORJSON

orjson = ORJSON()


@dataclass
class NewDataClass:
    hello: str = "world"


def create_app():
    app = Flask(__name__)
    orjson.init_app(app)  # Sets ORJSON as the default JSON encoder

    @app.route("/")
    def index():
        """
        Outputs a JSON response using the orjson library

        https://github.com/ijl/orjson
        """
        return {
            "timestamp": 1556283673.1523004,
            "task_uuid": "0ed1a1c3-050c-4fb9-9426-a7e72d0acfc7",
            "task_level": [1, 2, 1],
            "action_status": "started",
            "action_type": "main",
            "key": "value",
            "another_key": 123,
            "and_another": ["a", "b"],
            "today": datetime.now(),
            "dataclass": NewDataClass()
        }

    @app.post("/post")
    def accept_json():
        json = request.get_json()
        return json

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)

```