# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Files support for the RERO invenio instances."""

from invenio_db import db
from invenio_files_rest.models import Bucket
from invenio_records.models import RecordMetadataBase
from invenio_records_resources.records.models import FileRecordModelMixin
from sqlalchemy_utils.types import UUIDType


class RecordMetadata(db.Model, RecordMetadataBase):
    """Model for Record module metadata."""

    __tablename__ = "objects"
    bucket_id = db.Column(UUIDType, db.ForeignKey(Bucket.id))
    bucket = db.relationship(Bucket)


class FileRecordMetadata(db.Model, RecordMetadataBase, FileRecordModelMixin):
    """Model for Record files module."""

    __tablename__ = "objects_files"
    __record_model_cls__ = RecordMetadata
