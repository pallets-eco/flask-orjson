## Version 2.0.0

Released 2024-01-14

- Simplify how the library is used and configured.
- The `ORJSON` extension class is removed. Use `app.json = OrjsonProvider(app)`.
- `OrjsonProvider` has `option` and `default` attributes, or `dumps` takes them
  as keyword arguments.
- The provider does not have `sort_keys` or `compact` as arguments or
  attributes. Use `option` to set the relevant orjson flags instead.
- The `__version__` attribute is removed. Call `importlib.metadata.version` instead.
- `datetime` objects without a timezone (naive) use UTC.
- Export type annotations.
- Change license to MIT.
- Use PyPI trusted publishing.
- Use `src` directory layout.

## Version 1.2.0

Released 2023-12-11

- Python 3.8 compatibility.

## Version 1.1.0

Released 2023-12-10

- Add init arguments to control output format and `default` function.

## Version 1.0.3

Released 2023-12-08

- Fix use of `dumps` `kwargs`.

## Version 1.0.2

Released 2023-12-08

- Fix minimum orjson version.

## Version 1.0.1

Released 2023-12-01

- Update docs.

## Version 1.0.0

Released 2023-12-01

- Initial release.
