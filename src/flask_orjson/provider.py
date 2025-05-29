from __future__ import annotations

import typing as t
from decimal import Decimal

import orjson
from flask.json.provider import JSONProvider


def _default(o: t.Any) -> t.Any:
    if isinstance(o, Decimal):
        return str(o)

    if hasattr(o, "__html__"):
        return str(o.__html__())

    raise TypeError(f"Object of type {type(o).__name__} is not JSON serializable")


class OrjsonProvider(JSONProvider):
    """A :class:`~flask.json.provider.JSONProvider` that uses the fast
    `orjson <https://github.com/ijl/orjson>`__ library.
    """

    option: int | None = orjson.OPT_NAIVE_UTC
    """Option flags to pass to ``orjson.dumps``. Available flags are listed in
    the `orjson docs <https://github.com/ijl/orjson#option>`__. Multiple flags
    are combined using ``|`` bitwise or.

    By default the ``NAIVE_UTC`` flag is enabled, which assumes the UTC timezone
    for :mod:`datetime` objects that do not have a timezone.
    """

    default: t.Callable[[t.Any], t.Any] | None = staticmethod(_default)  # type: ignore[assignment]
    """Function to call to convert data in an unsupported type to a valid JSON
    type.

    By default, :class:`~decimal.Decimal`, and classes with an `__html__` method
    are supported, in addition to the extra types that orjson already supports.
    """

    def dumps(
        self,
        obj: t.Any,
        *,
        option: int | None = None,
        default: t.Callable[[t.Any], t.Any] | None = None,
        **kwargs: t.Any,
    ) -> str:
        """Serialize data as JSON.

        :param obj: The data to serialize.
        :param option: Option flags to pass to ``orjson.dumps``. Available flags
            are listed in the `orjson docs <https://github.com/ijl/orjson#option>`__.
            Multiple flags are combined using ``|`` bitwise or. Uses the
            :attr:`option` attribute if not given.
        :param default: Function to call to convert data in an unsupported type
            to a valid JSON type. Uses the :attr:`default` attribute if not
            given.
        :param kwargs: Any other keyword arguments are silently ignored.
        """
        if option is None:
            option = self.option

        if default is None:
            default = self.default

        return orjson.dumps(obj, option=option, default=default).decode()

    def loads(self, s: str | bytes, **kwargs: t.Any) -> t.Any:
        """Deserialize data as JSON.

        :param s: Text or UTF-8 bytes.
        :param kwargs: All keyword arguments are silently ignored.
        """
        return orjson.loads(s)
