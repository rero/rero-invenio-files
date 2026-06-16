# SPDX-FileCopyrightText: Fondation RERO+
# SPDX-License-Identifier: AGPL-3.0-or-later

"""Files support for the RERO invenio instances."""

from rero_invenio_files.records.services import FileServiceConfig, RecordServiceConfig

from .permissions import MockPermissionPolicy


class MockRecordServiceConfig(RecordServiceConfig):
    """Mock record service configuration."""

    permission_policy_cls = MockPermissionPolicy


class MockFileServiceConfig(FileServiceConfig):
    """Records files service configuration."""

    permission_policy_cls = MockPermissionPolicy
