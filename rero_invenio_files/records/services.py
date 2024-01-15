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
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""Files support for the RERO invenio instances."""

from invenio_records_resources.services import FileService as BaseFileService
from invenio_records_resources.services import (
    FileServiceConfig as BaseFileServiceConfig,
)
from invenio_records_resources.services import RecordService as BaseRecordService
from invenio_records_resources.services import (
    RecordServiceConfig as BaseRecordServiceConfig,
)
from invenio_records_resources.services.files.links import FileLink
from invenio_records_resources.services.records.components import FilesComponent

from .api import RecordWithFile
from .components import ThumbnailAndFulltextComponent
from .permissions import PermissionPolicy
from .schema import RecordSchema


class RecordServiceConfig(BaseRecordServiceConfig):
    """Record service configuration.

    Needs both configs, with File overwritting the record ones.
    """

    permission_policy_cls = PermissionPolicy
    record_cls = RecordWithFile
    schema = RecordSchema
    service_id = "records"


class FileServiceConfig(BaseFileServiceConfig):
    """Records files service configuration."""

    permission_policy_cls = PermissionPolicy
    record_cls = RecordWithFile
    file_links_item = {
        "self": FileLink("{+api}/records/{id}/files/{+key}"),
        "content": FileLink("{+api}/records/{id}/files/{+key}/content"),
        "commit": FileLink("{+api}/records/{id}/files/{+key}/commit"),
    }
    service_id = "records-files"
    components = BaseFileServiceConfig.components + [
        FilesComponent,
        ThumbnailAndFulltextComponent,
    ]


RecordFileService = BaseFileService
RecordService = BaseRecordService
