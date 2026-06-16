# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Files support for the RERO invenio instances."""

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import Schema, fields
from marshmallow_utils.fields import SanitizedUnicode


class MetadataSchema(Schema):
    """Record metadata schema class."""

    collections = fields.List(SanitizedUnicode())
    owners = fields.List(SanitizedUnicode())
    links = fields.List(SanitizedUnicode())
    files = fields.Dict()


class RecordSchema(BaseRecordSchema):
    """Record schema."""

    metadata = fields.Nested(MetadataSchema)
