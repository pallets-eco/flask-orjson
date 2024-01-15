# flask-orjson

A [Flask][]/[Quart][] {class}`~.flask.json.provider.JSONProvider` using the fast
[orjson][] library. Using this provider will significantly speed up reading JSON
data in requests and generating JSON responses.

[Flask]: https://flask.palletsprojects.com
[Quart]: https://quart.palletsprojects.com
[orjson]: https://github.com/ijl/orjson

## Usage

```python
from flask import Flask
from flask_orjson import OrjsonProvider

app = Flask(__name__)
json_provider = OrjsonProvider(app)
app.json = json_provider
```

## Dump Options

Orjson takes a number of options to control the accepted input as well as the
format of the output. Available flags are listed in the
[orjson docs](https://github.com/ijl/orjson#option). Multiple flags are combined
using `|` bitwise or.

By default, flask-orjson enables the `NAIVE_UTC` flag to treat
{class}`~datetime.datetime` objects without a timezone (naive) as being in UTC.

## Supported Types

Orjson has built-in support for serializing non-JSON types including
{class}`~datetime.datetime`, {class}`~datetime.date`,
{func}`~dataclasses.dataclass`, and {class}`~uuid.UUID`. Flask-orjson adds
support for {class}`~decimal.Decimal` and classes with an `__html__` method.

One difference from the default provider is {class}`~datetime.datetime` and
{class}`~datetime.date` are serialized using ISO 8601 format instead of RFC 822.
This is typically what libraries and users expect nowadays.

You can use the {attr}`~.OrjsonProvider.option` and
{attr}`~.OrjsonProvider.default` attributes to modify how non-JSON types are
serialized.

## Complex Data

It's possible to write a {attr}`~.OrjsonProvider.default` function to handle any
data. However, we recommend using a dedicated object serialization library to
first convert complex data to JSON types, before serializing that to JSON. This
gives you full control over how your data is represented, as well as the ability
to deserialize data in requests. Some such libraries include [cattrs][],
[Marshmallow][], and [Pydantic][].

[cattrs]: https://catt.rs
[marshmallow]: https://marshmallow.readthedocs.io
[Pydantic]: https://docs.pydantic.dev

```{toctree}
:hidden:

api
changes
license
```
