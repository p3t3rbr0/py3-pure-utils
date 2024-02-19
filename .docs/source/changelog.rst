Changelog
=========

v0.4.0 - [2024-02-19]
---------------------
* Add several tests (for `dt` module) for python3.10 only.
* Add new module - `debug` (utilities for debugging and development).
* Add new module - `profiler` (helper classes for working with the cProfile).
* Refactor .docs/Makefile
* Add support Python3.12 into ci scenario.
* Use flake8 explicitly into Makefile and ci scenario.
* Remove `pyproject-flake8` optional dependencies, because it's orphaned on github.

v0.3.0 - [2024-02-04]
---------------------
* Add new module - `dt` (utilities for working with datetime objects).

v0.2.0 - [2024-02-02]
---------------------
* Add new string utilities module.
* Fix coverage settings.
* Add short utilities description in README.
* Add new make commands (tests-cov-json, tests-cov-html).
* Remove run_tests.sh.
* Rename github workflow scenario.

v0.1.1 - [2024-02-01]
---------------------
* Add badges for gh-repo.
* Add new make-command: upload (for upload built packages to PyPI).
* Fix Makefile.
* Fix Sphinx docs.
* Fix package name in README.

v0.1.0 - [2024-02-01]
---------------------
* Create project repository with infrastructure:
  python project, github actions, makefile automations, docs, etc).
* Add a first general-purpose utility - metaclass for creating the singletons.
