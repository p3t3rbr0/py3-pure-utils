.DEFAULT_GOAL := help
.PHONY: deps-dev deps-docs deps-build deps build-sdist build-wheel build upload format lint tests clean help
MAKEFLAGS += --silent

# Aliases
PIP   = python -m pip
MYPY  = python -m mypy
BUILD = python -m build
ISORT = python -m isort
BLACK = python -m black
FLAKE = python -m pflake8
PYDOC = python -m pydocstyle

deps-dev:
	$(PIP) install '.[dev]' --upgrade

deps-docs:
	$(PIP) install '.[docs]' --upgrade

deps-build:
	$(PIP) install '.[build]' --upgrade

deps: deps-dev deps-docs deps-build

build-sdist:
	$(BUILD) --sdist

build-wheel:
	$(BUILD) --wheel

build: build-sdist build-wheel

upload:
	twine upload dist/*

format:
	$(BLACK) --line-length 100 --fast pure_utils/
	$(ISORT) pure_utils/
	$(BLACK) --line-length 100 --fast tests/
	$(ISORT) tests/

lint:
	printf "[flake8]: checking ... "
	$(FLAKE) pure_utils/ && printf "OK\n"
	printf "[mypy]: checking ... "
	$(MYPY) --install-types --non-interactive pure_utils/ && printf "OK\n"
	printf "[pydocstyle]: checking ... "
	$(PYDOC) pure_utils/ && printf "OK\n"

tests:
	./run_tests.sh

clean:
	rm -rf .pytest_cache/ .mypy_cache/ junit/ build/ dist/ coverage_report/
	find . -not -path './.venv*' -path '*/__pycache__*' -delete
	find . -not -path './.venv*' -path '*/*.egg-info*' -delete

help:
	echo
	echo "Usage:"
	echo "--------------------------------------------------------------------------------"
	echo "help\t\tShow this message."
	echo
	echo "deps-dev\tInstall only development dependencies."
	echo "deps-docs\tInstall only documentation dependencies."
	echo "deps-build\tInstall only build system dependencies."
	echo "deps\t\tInstall all dependencies."
	echo
	echo "build-sdist\tBuild a source distrib."
	echo "build-wheel\tBuild a pure python wheel distrib."
	echo "build\t\tBuild both distribs (source and wheel)."
	echo "upload\t\Upload built packages to PyPI."
	echo
	echo "test\t\tRun tests with coverage measure."
	echo "clean\t\tClean temporary files and caches."
	echo "format\t\tFromat the code (by black and isort)."
	echo "lint\t\tCheck code style and types (by flake8, pydocstyle and mypy)."
	echo
