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

from typing import List

from runway.common.utils import save_settings_to_dotenv
from runway.projects.api_client import fetch_joined_projects, fetch_user_project_role
from runway.projects.schemas import ProjectInfo
from runway.settings import settings


def get_joined_projects() -> List[ProjectInfo]:
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError(
            "RUNWAY_SDK_TOKEN is not set. Please login first.",
        )
    if not settings.RUNWAY_WORKSPACE_ID:
        raise ValueError(
            "RUNWAY_WORKSPACE_ID is not set. Please call set_joined_workspace() first.",
        )
    projects = fetch_joined_projects()
    for project in projects:
        project_id = project["id"]
        user_project_role = fetch_user_project_role(project_id)
        project["project_role"] = user_project_role["project_role"]
    return [ProjectInfo(**project) for project in projects]


def set_joined_project(project_id: int) -> None:
    projects = fetch_joined_projects()
    for project in projects:
        if project["id"] == project_id:
            settings.RUNWAY_PROJECT_ID = str(project_id)
            settings.RUNWAY_PROJECT_DIR = project["directory_name"]
            save_settings_to_dotenv()
            break
    else:
        raise ValueError(
            f"Project ID {project_id} not found in the joined projects. Please provide a valid project ID.",
        )
