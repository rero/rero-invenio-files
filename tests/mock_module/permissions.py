# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Files support for the RERO invenio instances."""

from invenio_records_permissions import RecordPermissionPolicy
from invenio_records_permissions.generators import AnyUser, SystemProcess


class MockPermissionPolicy(RecordPermissionPolicy):
    """."""

    can_search = [AnyUser(), SystemProcess()]
    can_read = [AnyUser(), SystemProcess()]
    can_create = [AnyUser(), SystemProcess()]
    can_update = [AnyUser(), SystemProcess()]
    can_delete = [AnyUser(), SystemProcess()]

    can_get_content_files = [AnyUser(), SystemProcess()]
    can_set_content_files = [AnyUser(), SystemProcess()]

    can_read_files = [AnyUser(), SystemProcess()]
    can_create_files = [AnyUser(), SystemProcess()]
    can_commit_files = [AnyUser(), SystemProcess()]
    can_update_files = [AnyUser(), SystemProcess()]
    can_delete_files = [AnyUser(), SystemProcess()]
