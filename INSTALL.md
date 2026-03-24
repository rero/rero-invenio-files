<!--
 RERO-Invenio-Files
 Copyright (C) 2024 RERO.

 This program is free software: you can redistribute it and/or modify
 it under the terms of the GNU Affero General Public License as published by
 the Free Software Foundation, version 3 of the License.

 This program is distributed in the hope that it will be useful,
 but WITHOUT ANY WARRANTY; without even the implied warranty of
 MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
 GNU Affero General Public License for more details.

 You should have received a copy of the GNU Affero General Public License
 along with this program. If not, see <http://www.gnu.org/licenses/>.
-->

# RERO-Invenio-Files Installation

## Requirements

- `git`
- `docker`, `docker-compose`
- `python`, `pip`, `pyenv`
- `uv`

## Installation

First, create your working directory and `cd` into it. Clone the project into this directory:

```console
git clone https://github.com/rero/rero-invenio-files.git
```

You need to install `uv`, it will handle the virtual environment creation for the project
in order to sandbox our Python environment, as well as manage the dependency installation,
among other things.

```console
pyenv install 3.12
cd rero-invenio-files
pyenv local 3.12
curl -LsSf https://astral.sh/uv/install.sh | sh
```

See the [uv installation documentation](https://docs.astral.sh/uv/getting-started/installation) for more detail.

Next, `cd` into the project directory and install all Python dependencies:

```console
cd rero-invenio-files
uv sync
```

## Testing

Run the test suite via the provided script:

```console
uv run poe run_tests
```
