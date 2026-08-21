<!--
SPDX-FileCopyrightText: Fondation RERO+
SPDX-License-Identifier: AGPL-3.0-or-later
-->

# rero-invenio-files Claude guide

## Overview

rero-invenio-files is a Python library providing files support for RERO Invenio instances. It ships a record API with attached files, automatic thumbnail generation and full-text extraction on file commit, a previewer for those files, and a PDF generator.

## Commands

All commands are run through uv's virtual env with `uv run`.

### Linting and formatting

**IMPORTANT:** After editing files, make sure that there are no errors in the formatting and linting.

```bash
uv run poe lint     # ruff check
uv run poe format   # ruff format
```

### Setup (done by humans)

Human developers will start the required containers and services on their own terms. Tests require DB, SEARCH, CACHE and MQ to be running; `run-tests.sh` brings them up itself through `docker-services-cli`.

## Architecture

### Extension

`REROInvenioFiles` in `ext.py` initializes the `RERO_FILES_*` config keys, then the services and resources. Service and resource classes are resolved from those config keys, so an instance can swap them (the tests do it in `tests/mock_module`). Registration into the invenio service and indexer registries happens in `api_finalize_app`, not in the extension, because invenio-records-resources may not be initialized yet. Blueprints are exposed by `views.py` through the `invenio_base` entry points.

### Records module

`records/models.py` maps the `objects` and `objects_files` tables. `records/api.py` defines `Record`, `RecordWithFile` (adds the `FilesField` and the bucket) and `FileRecord`; the two classes reference each other, hence the deferred `FileRecord.record_cls` assignment at the end of the module. `records/services.py` holds the service configs and the file link classes: `PreviewFileLink` only renders for previewable mime types, `ThumbFileLink` points at the generated thumbnail.

### Thumbnails and full text

`ThumbnailAndFulltextComponent` in `records/components.py` hooks `commit_file` and `delete_file`. Derived files are named by `change_filename_extension` (`test.pdf` becomes `test-pdf.jpg` and `test-pdf.txt`) and carry a `metadata.type` of `thumbnail` or `fulltext`, which is what stops the component from recursing on its own output and lets `delete_file` clean them up with the original. Thumbnails are capped at 200px: first page via pymupdf for PDFs, Pillow for images. Full-text extraction is pymupdf only, NFKC normalized, and returns `None` for encrypted or empty PDFs. Both are best effort: a failure is logged and the commit still succeeds.

### Previewer

`records/previewer.py` provides `preview` and `record_file_factory` to be plugged into the `RECORDS_UI_ENDPOINTS` and `PREVIEWER_RECORD_FILE_FACOTRY` config keys of the instance. That second key is misspelled in invenio-previewer itself, so the typo must be kept.

### PDF module

`PDFGenerator` in `pdf/__init__.py` subclasses `fpdf.FPDF`. It bundles the NotoSans fonts and picks a random logo and graph from `pdf/logos` and `pdf/graphs`. `render()` lays out the header, title, authors, summary box, paragraph and graph from the data dict given to the constructor.

## Code style

- Be clear and concise in docstrings; do not over-comment the code.
- Do not use Python type annotations (no `-> str`, `: str`, etc. in signatures).
- Ruff is configured in `pyproject.toml`: `line-length = 120` and the excluded files under `[tool.ruff]`, the enabled rule sets under `[tool.ruff.lint]`, and the pep257 docstring convention under `[tool.ruff.lint.pydocstyle]`.
- Since Python 3.14 (PEP 758), parentheses around multiple exception types are optional when the `except`/`except*` clause has no `as` target: `except AttributeError, UnboundLocalError:` is valid and equivalent to `except (AttributeError, UnboundLocalError):` — not the old Python 2 comma syntax. `ruff format` removes the parentheses in that case; this is expected, not a bug. Parentheses are still required when binding the exception: `except (AttributeError, UnboundLocalError) as error:`.
- Commit messages follow [Conventional Commits](https://www.conventionalcommits.org).

## Testing

- Tests use function-based style (no class-based tests).
- The project follows a test-driven development methodology. Each commit must be accompanied by tests that ensure that the functionality works as intended. Tests must follow DRY principles and should only test specific app behaviour and not the behaviour of external modules (e.g. invenio dependencies).
- `--doctest-modules` is active and `testpaths` includes `rero_invenio_files`, so any `>>>` example written in a docstring is collected and run as a test.
- `tests/conftest.py` overrides the service configs with the ones from `tests/mock_module` (permissions open enough to exercise the REST API), provides a temporary files `file_location`, and generates a real PDF through `PDFGenerator` as the `pdf_file` upload payload.
- Known vulnerabilities that cannot be fixed yet are ignored one by one in `run-tests.sh` with `add_exceptions`, each preceded by a comment naming the package and the version that fixes it.

### Running the tests (done by humans)

Human developers run tests from their consoles:

```bash
uv run poe run_tests    # full suite (pip-audit + lint + services + pytest)
uv run poe tests        # pytest only (services must already be running)
uv run poe tests_debug  # pytest -s -vv --no-cov
```
