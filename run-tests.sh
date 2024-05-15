#!/usr/bin/env bash
# -*- coding: utf-8 -*-
#
# RERO-Invenio-Files
# Copyright (C) 2024 RERO.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.


# Usage:
#   env DB=postgresql12 SEARCH=elasticsearch7 CACHE=redis MQ=rabbitmq ./run-tests.sh

# Quit on errors
set -o errexit

# Quit on unbound symbols
set -o nounset

# Always bring down docker services
function cleanup() {
    eval "$(docker-services-cli down --env)"
}
trap cleanup EXIT

pip_audit_exceptions=""
add_exceptions() {
  pip_audit_exceptions="$pip_audit_exceptions --ignore-vuln $1"""
}

# python -m check_manifest
python -m sphinx.cmd.build -qnNW docs docs/_build/html

# cryptography 43.0.3  GHSA-79v4-65xg-pq4g 44.0.1
add_exceptions "GHSA-79v4-65xg-pq4g"
# py           1.11.0  PYSEC-2022-42969
add_exceptions "PYSEC-2022-42969"
# werkzeug     2.2.3   PYSEC-2023-221      2.3.8,3.0.1
add_exceptions "PYSEC-2023-221"
# werkzeug     2.2.3   GHSA-2g68-c3qc-8985 3.0.3
add_exceptions "GHSA-2g68-c3qc-8985"
# werkzeug     2.2.3   GHSA-f9vj-2wh5-fj8j 3.0.6
add_exceptions "GHSA-f9vj-2wh5-fj8j"
# werkzeug     2.2.3   GHSA-q34m-jh98-gwm2 3.0.6
add_exceptions "GHSA-q34m-jh98-gwm2"
PIPAPI_PYTHON_LOCATION=`which python` pip-audit ${pip_audit_exceptions}

autoflake -r --remove-all-unused-imports --ignore-init-module-imports --quiet .

# TODO: Remove services below that are not neeed (fix also the usage note).
docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-elasticsearch} --cache ${CACHE:-redis} --mq ${MQ:-rabbitmq} --env
python -m pytest
tests_exit_code=$?
python -m sphinx.cmd.build -qnNW -b doctest docs docs/_build/doctest
exit "$tests_exit_code"
