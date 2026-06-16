# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Files support for the RERO invenio instances."""

from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
from invenio_records.systemfields import ConstantField, ModelField
from invenio_records_resources.records.api import FileRecord as FileRecordBase
from invenio_records_resources.records.api import Record as RecordBase
from invenio_records_resources.records.systemfields import (
    FilesField,
    IndexField,
    PIDField,
)

from . import models


class FileRecord(FileRecordBase):
    """Object record file API."""

    model_cls = models.FileRecordMetadata
    # defined later
    record_cls = None


class Record(RecordBase):
    """Record class to store file metadata."""

    # Configuration
    model_cls = models.RecordMetadata
    # System fields
    schema = ConstantField("$schema", "local://records/record-v1.0.0.json")
    # expires_at = ModelField()
    index = IndexField("records-record-v1.0.0", search_alias="records")
    # persistant identifier
    pid = PIDField("id", provider=RecordIdProviderV2)


class RecordWithFile(Record):
    """Record with files."""

    # files field
    files = FilesField(store=False, file_cls=FileRecord)
    # buckets
    bucket_id = ModelField()
    bucket = ModelField(dump=False)


# record class
FileRecord.record_cls = RecordWithFile
