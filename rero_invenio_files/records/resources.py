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
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Files support for the RERO invenio instances."""

from urllib.parse import quote

from invenio_records_resources.resources import FileResource as BaseFileResource
from invenio_records_resources.resources import (
    FileResourceConfig as BaseFileResourceConfig,
)
from invenio_records_resources.resources import RecordResource as BaseRecordResource
from invenio_records_resources.resources import (
    RecordResourceConfig as BaseRecordResourceConfig,
)
from invenio_records_resources.resources.files.resource import resource_requestctx


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

    def read_content(self):
        """Read file content and set proper Content-Disposition header."""
        # Get the response from the base class
        response = super().read_content()

        # Get the file key from the request context
        file_key = resource_requestctx.view_args["key"]

        # Set RFC 6266 / RFC 5987 compliant Content-Disposition header:
        # - filename: latin-1-safe fallback for legacy clients
        # - filename*: UTF-8 encoded per RFC 5987 for full Unicode support
        filename_latin1 = file_key.encode("latin-1", errors="replace").decode("latin-1")
        filename_star = "UTF-8''" + quote(file_key, encoding="utf-8", safe="")
        response.headers["Content-Disposition"] = f'attachment; filename="{filename_latin1}"; filename*={filename_star}'

        return response
