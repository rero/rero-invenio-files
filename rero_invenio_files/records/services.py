# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Files support for the RERO invenio instances."""

from invenio_records_resources.services import FileService as BaseFileService
from invenio_records_resources.services import (
    FileServiceConfig as BaseFileServiceConfig,
)
from invenio_records_resources.services import RecordService as BaseRecordService
from invenio_records_resources.services import (
    RecordServiceConfig as BaseRecordServiceConfig,
)
from invenio_records_resources.services.base import ExternalLink
from invenio_records_resources.services.records.components import FilesComponent
from invenio_records_resources.services.records.links import RecordEndpointLink

from .api import RecordWithFile
from .components import ThumbnailAndFulltextComponent
from .permissions import PermissionPolicy
from .schema import RecordSchema


class FileExternalLink(ExternalLink):
    """Non-deprecated replacement for FileLink with file key variable."""

    @staticmethod
    def vars(file_record, variables):
        """Variables for the URI template."""
        variables.update({"key": file_record.key})


class PreviewFileLink(FileExternalLink):
    """Add the preview link only for some document type."""

    def should_render(self, obj, ctx):
        """Determine if the link should be rendered."""
        if obj.get("metadata", {}).get("type") in ["thumbnail", "fulltext"]:
            return False
        # here we cannot use invenio previewer as it is available only on ui
        # pdf is supported
        if not hasattr(obj.file, "mimetype"):
            return False
        return obj.file.mimetype in ["application/pdf", "image/jpeg", "image/png"]


class ThumbFileLink(PreviewFileLink):
    """Add the thumbnail file name variable to generate the thumbnail links."""

    @staticmethod
    def vars(file_record, variables):
        """Variables for the URI template."""
        variables.update({"thumb": ThumbnailAndFulltextComponent.change_filename_extension(file_record.key, "jpg")})


class RecordServiceConfig(BaseRecordServiceConfig):
    """Record service configuration.

    Needs both configs, with File overwritting the record ones.
    """

    # permission policiy
    permission_policy_cls = PermissionPolicy
    # record class
    record_cls = RecordWithFile
    # marshmallow schema
    schema = RecordSchema
    links_item = {
        "self": RecordEndpointLink("records.read"),
    }
    service_id = "records"


class FileServiceConfig(BaseFileServiceConfig):
    """Records files service configuration."""

    # permission policy
    permission_policy_cls = PermissionPolicy
    # record class
    record_cls = RecordWithFile
    # API links
    file_links_item = {
        "self": FileExternalLink("{+api}/records/{id}/files/{+key}"),
        "content": FileExternalLink("{+api}/records/{id}/files/{+key}/content"),
        "commit": FileExternalLink("{+api}/records/{id}/files/{+key}/commit"),
        "preview": PreviewFileLink("{+ui}/records/preview/{id}/{+key}"),
        "thumbnail": ThumbFileLink("{+api}/records/{id}/files/{+thumb}/content"),
    }
    service_id = "records-files"
    # component processors
    components = [
        *BaseFileServiceConfig.components,
        FilesComponent,
        ThumbnailAndFulltextComponent,
    ]


# service classes
RecordFileService = BaseFileService
RecordService = BaseRecordService
