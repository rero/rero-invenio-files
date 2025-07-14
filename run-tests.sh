#!/usr/bin/env bash
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
#   env DB=postgresql15 SEARCH=elasticsearch7 CACHE=redis MQ=rabbitmq ./run-tests.sh

# COLORS for messages
NC='\033[0m'                    # Default color
INFO_COLOR='\033[1;97;44m'      # Bold + white + blue background
SUCCESS_COLOR='\033[1;97;42m'   # Bold + white + green background
ERROR_COLOR='\033[1;97;41m'     # Bold + white + red background

# MESSAGES
msg() {
  echo -e "${1}" 1>&2
}
# Display a colored message
# More info: https://misc.flogisoft.com/bash/tip_colors_and_formatting
# $1: choosen color
# $2: title
# $3: the message

colored_msg() {
  msg "${1}[${2}]: ${3}${NC}"
}

info_msg() {
  colored_msg "${INFO_COLOR}" "INFO" "${1}"
}

error_msg() {
  colored_msg "${ERROR_COLOR}" "ERROR" "${1}"
}

error_msg+exit() {
    error_msg "${1}" && exit 1
}

success_msg() {
  colored_msg "${SUCCESS_COLOR}" "SUCCESS" "${1}"
}

success_msg+exit() {
  colored_msg "${SUCCESS_COLOR}" "SUCCESS" "${1}" && exit 0
}

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
# sphinx-build -qnNW docs docs/_build/html

info_msg "Check vulnerabilities:"
# py 1.11.0  PYSEC-2022-42969
add_exceptions "PYSEC-2022-42969"
# urllib3 1.26.20 GHSA-pq67-6m6q-mj2v 2.5.0
add_exceptions "GHSA-pq67-6m6q-mj2v"
pip-audit ${pip_audit_exceptions}

info_msg "Test formatting:"
ruff format . --check
info_msg "Test linting:"
ruff check

# TODO: Remove services below that are not neeed (fix also the usage note).
docker-services-cli up --db ${DB:-postgresql} --search ${SEARCH:-elasticsearch} --cache ${CACHE:-redis} --mq ${MQ:-rabbitmq} --env
pytest
tests_exit_code=$?
exit "$tests_exit_code"
