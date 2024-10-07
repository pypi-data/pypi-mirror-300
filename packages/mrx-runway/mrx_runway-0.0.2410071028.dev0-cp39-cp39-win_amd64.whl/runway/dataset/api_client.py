#
#  MAKINAROCKS CONFIDENTIAL
#  ________________________
#
#  [2017] - [2024] MakinaRocks Co., Ltd.
#  All Rights Reserved.
#
#  NOTICE:  All information contained herein is, and remains
#  the property of MakinaRocks Co., Ltd. and its suppliers, if any.
#  The intellectual and technical concepts contained herein are
#  proprietary to MakinaRocks Co., Ltd. and its suppliers and may be
#  covered by U.S. and Foreign Patents, patents in process, and
#  are protected by trade secret or copyright law. Dissemination
#  of this information or reproduction of this material is
#  strictly forbidden unless prior written permission is obtained
#  from MakinaRocks Co., Ltd.
from typing import BinaryIO, Final, Optional

import requests

from runway.common.api_client import api_client
from runway.common.utils import exception_handler, exclude_none
from runway.model_registry.values import WorkloadType

# NOTE module-hierarchy 가 맞지 않기 때문에 rev2 보다 큰 revision 이 생성되면 수정되어야 한다.
from runway.settings import settings

REQUEST_TIMEOUT: Final[int] = 10


def upload_data_snapshot_and_version(
    name: str,
    binary: BinaryIO,
    description: Optional[str] = None,
) -> dict:
    if settings.launch_params is None or settings.launch_params.source is None:
        raise ValueError("There are no launch parameters")

    if description is not None and len(description) > 100:
        raise ValueError("Description must be less than 100 characters")

    # TODO 나중에는 참조하는 코드가 없어야 한다...
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        response = exception_handler(
            requests.post(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    f"/v1/link/workspaces/{settings.RUNWAY_WORKSPACE_ID}"
                    f"/projects/{settings.RUNWAY_PROJECT_ID}"
                    "/data-snapshots/sdk"
                ),
                headers={"Authorization": f"Bearer {settings.TOKEN}"},
                files={"file": binary},
                data=exclude_none(
                    {
                        "name": name,
                        "description": description,
                    },
                ),
                timeout=REQUEST_TIMEOUT,
            ),
        )

        return response.json()
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        response = exception_handler(
            requests.post(
                (
                    f"http://{settings.RUNWAY_API_SERVER_URL}"
                    "/v1/internal/workspaces/projects"
                    f"/{settings.RUNWAY_PROJECT_ID}/data-snapshots/sdk"
                ),
                files={"file": binary},
                data=exclude_none(
                    {
                        "user_id": settings.RUNWAY_USER_ID,
                        "name": name,
                        "description": description,
                        "argo_workflow_run_id": settings.ARGO_WORKFLOW_RUN_ID,
                    },
                ),
                timeout=REQUEST_TIMEOUT,
            ),
        )

        return response.json()
    else:
        raise ValueError(
            "entity name of launch parameters should be in [dev_instance, pipeline]",
        )


def sdk_create_data_snapshot(
    name: str,
    description: Optional[str] = None,
    exist_ok: bool = False,
) -> dict:
    """
    Using SDK token, create a new data snapshot in the current project
    """

    api_path_format: str = "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots"
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
    )

    data = exclude_none(
        {
            "name": name,
            "description": description,
            "exist_ok": exist_ok,
        },
    )

    response: dict = api_client.post(api_path, data=data)

    return response


def internal_create_data_snapshot(
    name: str,
    description: Optional[str] = None,
    exist_ok: bool = False,
) -> dict:
    """
    Without any token, create the new data snapshot in the current project.
    Intended to be used in the internal environment(pipeline).
    """

    api_path_format: str = "/v1/internal/workspaces/projects/{pid}/data-snapshots"
    api_path: str = api_path_format.format(pid=settings.RUNWAY_PROJECT_ID)

    data = exclude_none(
        {
            "user_id": settings.RUNWAY_USER_ID,
            "name": name,
            "description": description,
            "exist_ok": exist_ok,
        },
    )

    response: dict = api_client.post(api_path, data=data)

    return response


def sdk_get_data_snapshot_by_name(name: str) -> dict:
    """
    Using SDK token, get a data snapshot by name.
    Name should be matched exactly
    """
    api_path_format: str = "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/name"
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
    )

    params = {"name": name}

    response = api_client.get(api_path, params=params)

    return response


def internal_get_data_snapshot_by_name(name: str) -> dict:
    """
    Without any token, get the data snapshot in the current project.
    Intended to be used in the internal environment(pipeline).

    Name should be matched exactly
    """
    api_path_format: str = "/v1/internal/workspaces/projects/{pid}/data-snapshots/name"
    api_path: str = api_path_format.format(pid=settings.RUNWAY_PROJECT_ID)

    params = {"name": name, "user_id": settings.RUNWAY_USER_ID}

    response = api_client.get(api_path, params=params)

    return response


def sdk_create_data_snapshot_version(
    data_snapshot_id: int,
    description: Optional[str] = None,
) -> dict:
    """
    Using SDK token, create a new data snapshot version.
    """
    api_path_format: str = (
        "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/{did}/versions"
    )
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
        did=data_snapshot_id,
    )

    data = exclude_none({"description": description})

    response: dict = api_client.post(api_path, data=data)

    return response


def sdk_get_data_snapshot_list() -> dict:

    api_path_format: str = "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots"
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
    )

    response: dict = api_client.get(api_path)

    return response


def sdk_get_data_snapshot_detail(data_snapshot_id: int) -> dict:

    api_path_format: str = (
        "/v1/sdk/workspaces/{wid}/projects/{pid}/data-snapshots/{did}"
    )
    api_path: str = api_path_format.format(
        wid=settings.RUNWAY_WORKSPACE_ID,
        pid=settings.RUNWAY_PROJECT_ID,
        did=data_snapshot_id,
    )

    response: dict = api_client.get(api_path)

    return response


def internal_create_data_snapshot_version(
    data_snapshot_id: int,
    description: Optional[str] = None,
) -> dict:
    """
    Without any token, create a new data snapshot version.
    Intended to be used in the internal environment(pipeline).
    """
    api_path_format: str = (
        "/v1/internal/workspaces/projects/{pid}/data-snapshots/{pid}/versions"
    )
    api_path: str = api_path_format.format(
        pid=settings.RUNWAY_PROJECT_ID,
        did=data_snapshot_id,
    )

    data = exclude_none(
        {
            "user_id": settings.RUNWAY_USER_ID,
            "description": description,
            "argo_workflow_run_id": settings.ARGO_WORKFLOW,
        },
    )

    response: dict = api_client.post(api_path, data=data)

    return response
