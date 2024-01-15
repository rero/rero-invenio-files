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

from invenio_records_resources.services.records.schema import BaseRecordSchema
from marshmallow import INCLUDE, Schema, fields
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