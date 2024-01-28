Make commands
=============

Actual for contributors only.

Dependencies
------------

- ``make deps`` - Install all dependencies.
- ``make deps-dev`` - Install only development dependencies.
- ``make deps-build`` - Install only build system dependencies.

Building
--------

- ``make build`` - Build both distribs (source and wheel).
- ``make build-sdist`` - Build a source distrib.
- ``make build-wheel`` - Build a pure python wheel distrib.

Development
-----------

- ``make format`` - Fromat the code (by black and isort).
- ``make lint`` - Check code style and types (by flake8, pydocstyle and mypy).
- ``make tests`` - Run tests with coverage measure.
- ``make clean`` - Clean temporary files and caches.
