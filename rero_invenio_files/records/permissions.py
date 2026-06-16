# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Files support for the RERO invenio instances."""

from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess


class PermissionPolicy(RecordPermissionPolicy):
    """Record and files permission policies."""

    can_search = [AnyUser(), SystemProcess()]
    can_read = [AnyUser(), SystemProcess()]
    can_create = [SystemProcess()]
    can_update = [SystemProcess()]
    can_delete = [SystemProcess()]

    can_get_content_files = [AnyUser(), SystemProcess()]
    can_set_content_files = [SystemProcess()]

    can_read_files = [AnyUser(), SystemProcess()]
    can_create_files = [SystemProcess()]
    can_commit_files = [SystemProcess()]
    can_update_files = [SystemProcess()]
    can_delete_files = [SystemProcess()]
