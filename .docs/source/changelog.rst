Changelog
=========

v0.5.0 - [2024-02-25]
---------------------
* Update versions build and dev dependencies.
* Add new module - `containers` (utilities for working with data containers).

v0.4.1 - [2024-02-20]
---------------------
* Refactor imports into tests.
* Rename `dt` module to `datetime`.
* Add `_internal` subpackage (with "private" modules).
* Refactor variables into `debug`, `profiler` and `_internal/*` modules.

v0.4.0 - [2024-02-19]
---------------------
* Refactor .docs/Makefile.
* Add support Python3.12 into ci scenario.
* Use flake8 explicitly into Makefile and ci scenario.
* Add several tests (for `dt` module) for python3.10 only.
* Add new module - `debug` (utilities for debugging and development).
* Add new module - `profiler` (helper classes for working with the cProfile).
* Remove `pyproject-flake8` optional dependencies, because it's orphaned on github.

v0.3.0 - [2024-02-04]
---------------------
* Add new module - `dt` (utilities for working with datetime objects).

v0.2.0 - [2024-02-02]
---------------------
* Remove run_tests.sh.
* Fix coverage settings.
* Rename github workflow scenario.
* Add new string utilities module.
* Add short utilities description in README.
* Add new make commands (tests-cov-json, tests-cov-html).

v0.1.1 - [2024-02-01]
---------------------
* Fix Makefile.
* Fix Sphinx docs.
* Add badges for gh-repo.
* Fix package name in README.
* Add new make-command: upload (for upload built packages to PyPI).

v0.1.0 - [2024-02-01]
---------------------
* Create project repository with infrastructure:
  python project, github actions, makefile automations, docs, etc).
* Add a first general-purpose utility - metaclass for creating the singletons.
