#!/bin/sh

#
# Usage.
#
# For all tests:
# ./run_tests.sh
#
# For single test file:
# ./run_tests.sh tests/test_common.py
#

set -eu

python -m pytest --cov pure_utils/ \
                 --cov-report term \
                 --cov-report json \
                 --cov-report html \
                 ${1:-tests/}
