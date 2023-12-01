"""Flask with UltraJSON."""

import dataclasses
import decimal
import typing as t
import uuid
from datetime import date

import orjson
from flask import Flask
from flask.json.provider import JSONProvider
from flask.wrappers import Response
from werkzeug.http import http_date

__version__ = "1.0.0"


def _default(o: t.Any) -> t.Any:
    if isinstance(o, date):
        return http_date(o)

    if isinstance(o, (decimal.Decimal, uuid.UUID)):
        return str(o)

    if dataclasses and dataclasses.is_dataclass(o):
        return dataclasses.asdict(o)

    if hasattr(o, "__html__"):
        return str(o.__html__())

    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


class ORJSONProvider(JSONProvider):
    """Provide JSON operations using the orjson
    library. Serializes the following additional data types:

    -   :class:`datetime.datetime` and :class:`datetime.date` are
        serialized to :rfc:`822` strings. This is the same as the HTTP
        date format.
    -   :class:`uuid.UUID` is serialized to a string.
    -   :class:`dataclasses.dataclass` is passed to
        :func:`dataclasses.asdict`.
    -   :class:`~markupsafe.Markup` (or any object with a ``__html__``
        method) will call the ``__html__`` method to get a string.
    """

    default: t.Callable[[t.Any], t.Any] = staticmethod(_default)  # type: ignore[assignment]
    """Apply this function to any object that :meth:`orjson.dumps` does
    not know how to serialize. It should return a valid JSON type or
    raise a ``TypeError``.
    """

    sort_keys = True
    """Sort the keys in any serialized dicts. This may be useful for
    some caching situations, but can be disabled for better performance.
    When enabled, keys must all be strings, they are not converted
    before sorting.
    """

    compact: bool | None = None
    """If ``True``, or ``None`` out of debug mode, the :meth:`response`
    output will not add indentation, newlines, or spaces. If ``False``,
    or ``None`` in debug mode, it will use a non-compact representation.
    """

    mimetype = "application/json"
    """The mimetype set in :meth:`response`."""

    def dumps(self, obj: t.Any, **kwargs: t.Any) -> str:
        """Serialize data as JSON to a string.

        Keyword arguments are passed to :func:`orjson.dumps`. Sets some
        parameter defaults from the :attr:`default`,
        :attr:`ensure_ascii`, and :attr:`sort_keys` attributes.

        :param obj: The data to serialize.
        :param kwargs: Passed to :func:`orjson.dumps`.
        """
        kwargs.setdefault("default", self.default)

        if self.sort_keys:
            if "compact" in kwargs:
                return orjson.dumps(
                    obj, option=orjson.OPT_SORT_KEYS | orjson.OPT_INDENT_2, **kwargs
                ).decode("utf-8")

            return orjson.dumps(obj, option=orjson.OPT_SORT_KEYS, **kwargs).decode(
                "utf-8"
            )

        if "compact" in kwargs:
            return orjson.dumps(obj, option=orjson.OPT_INDENT_2, **kwargs).decode(
                "utf-8"
            )

        return orjson.dumps(obj, **kwargs).decode("utf-8")

    def loads(self, s: str | bytes, **kwargs: t.Any) -> t.Any:
        """Deserialize data as JSON from a string or bytes.

        :param s: Text or UTF-8 bytes.
        :param kwargs: Passed to :func:`orjson.loads`.
        """
        return orjson.loads(s)

    def response(self, *args: t.Any, **kwargs: t.Any) -> Response:
        """Serialize the given arguments as JSON, and return a
        :class:`~flask.Response` object with it. The response mimetype
        will be "application/json" and can be changed with
        :attr:`mimetype`.

        If :attr:`compact` is ``False`` or debug mode is enabled, the
        output will be formatted to be easier to read.

        Either positional or keyword arguments can be given, not both.
        If no arguments are given, ``None`` is serialized.

        :param args: A single value to serialize, or multiple values to
            treat as a list to serialize.
        :param kwargs: Treat as a dict to serialize.
        """
        obj = self._prepare_response_obj(args, kwargs)

        if (self.compact is None and self._app.debug) or self.compact is False:
            return self._app.response_class(
                f"{self.dumps(obj)}\n", mimetype=self.mimetype
            )

        return self._app.response_class(
            f"{self.dumps(obj, compact=True)}\n", mimetype=self.mimetype
        )


class ORJSON:
    def __init__(self, app: t.Optional[Flask] = None) -> None:
        if app is not None:
            self.init_app(app)

    def init_app(self, app: Flask) -> None:
        if "orjson" in app.extensions:
            raise RuntimeError("Flask app already initialized for orjson")

        app.extensions["orjson"] = self
        app.json = ORJSONProvider(app)
