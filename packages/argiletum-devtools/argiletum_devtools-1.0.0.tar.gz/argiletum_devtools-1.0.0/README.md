# Argiletum development tools

![GitHub License](https://img.shields.io/github/license/argiletum/argiletum-devtools)
[![pypi](https://img.shields.io/pypi/v/argiletum-devtools.svg#1.0.0)](https://pypi.python.org/pypi/argiletum-devtools)
[![versions](https://img.shields.io/pypi/pyversions/argiletum-devtools.svg)](https://pypi.org/project/argiletum-devtools)

This is a collection of development tools used by [Argiletum](https://argiletum.io) and its plugins:

* [Bump My Version](https://callowayproject.github.io/bump-my-version/)
* [genbadge](https://smarie.github.io/python-genbadge/)
* [mypy](https://mypy.readthedocs.io/)
* [Pyright](https://microsoft.github.io/pyright/)
* [pytest](https://docs.pytest.org/)
* [pytest-cov](https://pytest-cov.readthedocs.io/)
* [Ruff](https://docs.astral.sh/ruff/)
* [tox](https://tox.wiki/)


## Usage

```shell
$ uv add --dev argiletum-devtools
```

## Development

Install [Task](https://taskfile.dev) and [uv](https://docs.astral.sh/uv/).

```shell
$ uv sync
$ task --list
```

Typical operations:

```shell
$ task lint
$ task format
$ task bump -- patch
$ task build
```
