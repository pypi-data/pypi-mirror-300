# MAKINAROCKS CONFIDENTIAL
# ________________________
#
# [2017] - [2024] MakinaRocks Co., Ltd.
# All Rights Reserved.
#
# NOTICE:  All information contained herein is, and remains
# the property of MakinaRocks Co., Ltd. and its suppliers, if any.
# The intellectual and technical concepts contained herein are
# proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
# covered by U.S. and Foreign Patents, patents in process, and
# are protected by trade secret or copyright law. Dissemination
# of this information or reproduction of this material is
# strictly forbidden unless prior written permission is obtained
# from MakinaRocks Co., Ltd.

import os
from typing import List

from runway.common.utils import save_settings_to_dotenv
from runway.settings import settings
from runway.workspaces.api_client import fetch_joined_workspaces
from runway.workspaces.schemas import WorkspaceInfo


def get_joined_workspaces() -> List[WorkspaceInfo]:
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError(
            "RUNWAY_SDK_TOKEN is not set. Please login first.",
        )
    workspaces = fetch_joined_workspaces()
    return [WorkspaceInfo(**workspace) for workspace in workspaces]


def set_joined_workspace(workspace_id: int) -> None:
    settings.RUNWAY_WORKSPACE_ID = str(workspace_id)
    os.environ["RUNWAY_WORKSPACE_ID"] = str(workspace_id)

    save_settings_to_dotenv()
