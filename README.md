## bloom

A compact (?) library for Discord.

### Why?

I want to use `trio`.

### Why should I use this?

You shouldn't. At least, not at the moment.

### Development Commands

Short reference for myself:

- install with `poetry install`
- generate docs with `python -m sphinx -M html docs _build`
- autoreload docs with `sphinx-autobuild docs _build --watch bloom`
- typecheck with `mypy . --strict`
- stylecheck (?) with `flake8 bloom` or `pylint bloom`
- fix imports with `isort bloom`
- test with `pytest`
- autoformat with `black .`

TODO: write more. or don't. that's a thing too.
