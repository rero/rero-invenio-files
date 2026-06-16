# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Files support for the RERO invenio instances."""

from invenio_records_resources.resources import FileResource as BaseFileResource
from invenio_records_resources.resources import (
    FileResourceConfig as BaseFileResourceConfig,
)
from invenio_records_resources.resources import RecordResource as BaseRecordResource
from invenio_records_resources.resources import (
    RecordResourceConfig as BaseRecordResourceConfig,
)


class RecordResourceConfig(BaseRecordResourceConfig):
    """Record resource configuration."""

    url_prefix = "/records"
    blueprint_name = "records"


class RecordResource(BaseRecordResource):
    """Record resource"."""


class FileResourceConfig(BaseFileResourceConfig):
    """Record file resource configuration."""

    url_prefix = "/records/<pid_value>"
    blueprint_name = "records_files"


class FileResource(BaseFileResource):
    """Record file resource."""
