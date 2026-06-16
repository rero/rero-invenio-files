<!--
SPDX-FileCopyrightText: Fondation RERO+
SPDX-License-Identifier: AGPL-3.0-or-later
-->

# RERO-Invenio-Files

[![Github actions
status](https://github.com/rero/rero-invenio-files/actions/workflows/continuous-integration-test.yml/badge.svg)](https://github.com/rero/rero-invenio-files/actions/workflows/continuous-integration-test.yml)
[![Release
Number](https://img.shields.io/github/tag/rero/rero-invenio-files.svg)](https://github.com/rero/rero-invenio-files/releases/latest)
[![Downloads](https://img.shields.io/pypi/dm/rero-invenio-files.svg)](https://pypi.python.org/pypi/rero-invenio-files)
[![License](https://img.shields.io/badge/License-AGPL%20v3-blue.svg)](http://www.gnu.org/licenses/agpl-3.0.html)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)

Files support for the RERO invenio instances.

## Install

`rero-invenio-files` is published on [PyPI](https://pypi.org/project/rero-invenio-files/).
Add it to your Invenio instance like any other dependency:

```console
pip install rero-invenio-files
```

Or, if you manage your instance with `uv`:

```console
uv add rero-invenio-files
```

The package registers itself through Invenio entry points, so no further wiring
is required.

## Development setup

To work on `rero-invenio-files` itself, clone the repository and install it in a
sandboxed environment managed by [`uv`](https://docs.astral.sh/uv/):

```console
git clone https://github.com/rero/rero-invenio-files.git
cd rero-invenio-files
uv sync
```

`uv sync` creates the virtual environment and installs every dependency,
including the development tools. If you need a specific Python version, `uv` can
provide it:

```console
uv python install 3.12
```

### Testing

Run the test suite via the provided task:

```console
uv run poe run_tests
```
