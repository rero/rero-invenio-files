# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Flask views."""

from flask import Blueprint

blueprint = Blueprint("rero_invenio_files", __name__)


def create_records_blueprint_from_app(app):
    """Create records blueprint for invenio-records-resources."""
    return app.extensions["rero-invenio-files"].records_resource.as_blueprint()


def create_records_files_blueprint_from_app(app):
    """Create records-files blueprint for invenio-records-resources."""
    return app.extensions["rero-invenio-files"].records_files_resource.as_blueprint()
