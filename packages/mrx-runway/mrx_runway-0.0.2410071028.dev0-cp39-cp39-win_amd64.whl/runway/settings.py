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
import json
import os
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from pydantic import BaseModel, BaseSettings, Field, root_validator, validator

# TODO logger 설정 필요
logger = None


class RunwaySource(BaseModel):
    entityname: str
    resource_id: int


class RunwayLinkSource(RunwaySource):
    entityname: Literal["dev_instance"]


class RunwayPipelineSource(RunwaySource):
    entityname: Literal["pipeline"]
    run_uuid: Optional[str]
    pipeline_id: int
    pipeline_version_id: int


class MLFlowModelRegistryData(BaseModel):
    type: Literal["mlflow"]
    version: str
    url: str
    storage_url: str
    access_key_id: str
    secret_access_key: str
    token: Optional[str]
    user: Optional[str]
    password: Optional[str]


class WandbModelRegistryData(BaseModel):
    type: Literal["wandb"]
    api_url: str
    api_key: str
    web_url: Optional[str] = None


class RunwayModelRegistry(BaseModel):
    id: Optional[int] = None
    data: Optional[Union[MLFlowModelRegistryData, WandbModelRegistryData]] = Field(
        ...,
        discriminator="type",
    )


class RunwayContainerRegistry(BaseModel):
    id: Optional[int] = None
    registry_server: Optional[str] = None


class RunwayLaunchParameters(BaseModel):
    source: Optional[Union[RunwayPipelineSource, RunwayLinkSource]] = Field(
        ...,
        discriminator="entityname",
    )
    notebook_name: Optional[str] = None
    container_image_name: Optional[str] = None


class SystemSettings(BaseSettings):  # type: ignore
    RUNWAY_WORKSPACE_ID: Optional[str] = None
    RUNWAY_PROJECT_ID: Optional[str] = None
    RUNWAY_PROJECT_DIR: Optional[str] = None
    RUNWAY_USER_ID: Optional[str] = None
    ARGO_WORKFLOW_RUN_ID: Optional[str] = None
    RUNWAY_API_SERVER_URL: Optional[str] = None  # backend api server hostname
    RUNWAY_MODEL_REGISTRY: Optional[str] = None  # model registry: '{"id": ...}'
    RUNWAY_CONTAINER_REGISTRY: Optional[str] = None  # container registry: '{"id": ...}'
    RUNWAY_LANUCH_PARAMETERS: Optional[
        str
    ] = None  # launch parameters: '{"source": {"entityname": "training-pipelines/links", "resource_id": 1}}'
    # TODO LANUCH -> LAUNCH for all in another PR
    RUNWAY_AUTH_BEARER_TOKEN: Optional[str] = None
    RUNWAY_API_PROTOCOL: Optional[str] = "http"
    RUNWAY_API_VERSION: Optional[str] = "v1"
    RUNWAY_API_PREFIX: Optional[str] = "sdk"
    RUNWAY_SDK_TOKEN: Optional[str] = None
    TOKEN: Optional[str] = None
    RUNWAY_PIPELINE_IMAGE_NAME: Optional[str] = None
    MAX_GRPC_MESSAGE_LENGTH: int = 64 * 1024 * 1024  # 64 MiB
    # Ref) https://makinarocks.atlassian.net/browse/RWAY-7173?focusedCommentId=47257

    RUNNING_IN_KUBERNETES: bool = True

    model_registry: RunwayModelRegistry = Field(default=None, exclude=True)  # type: ignore
    container_registry: RunwayContainerRegistry = Field(default=None, exclude=True)  # type: ignore
    launch_params: RunwayLaunchParameters = Field(default=None, exclude=True)  # type: ignore

    class Config:
        env_file: str = str(Path.home() / ".mrx-runway.env")
        env_file_encoding: str = "utf-8"
        required_env_vars: List[str] = [
            "RUNWAY_WORKSPACE_ID",
            "RUNWAY_PROJECT_ID",
            "RUNWAY_SDK_TOKEN",
            "TOKEN",
        ]

    @root_validator(pre=True)
    def do_after_validator(cls, values: Dict[str, Any]) -> Dict[str, Any]:
        for dst, src, _cls in [
            ("model_registry", "RUNWAY_MODEL_REGISTRY", RunwayModelRegistry),
            (
                "container_registry",
                "RUNWAY_CONTAINER_REGISTRY",
                RunwayContainerRegistry,
            ),
            ("launch_params", "RUNWAY_LANUCH_PARAMETERS", RunwayLaunchParameters),
        ]:
            src_value = values.get(src)
            if src_value is None:
                continue

            try:
                values[dst] = _cls(**json.loads(src_value))
            except Exception as e:
                ...

        return values

    @validator("RUNNING_IN_KUBERNETES", pre=True)
    def validate_running_in_kubernetes(cls, _: bool) -> bool:
        token_path = "/var/run/secrets/kubernetes.io/serviceaccount/token"
        return os.path.isfile(token_path)

    @property
    def grpc_options(self) -> List[Tuple[str, int]]:
        return [
            ("grpc.max_message_length", self.MAX_GRPC_MESSAGE_LENGTH),
            ("grpc.max_receive_message_length", self.MAX_GRPC_MESSAGE_LENGTH),
            ("grpc.max_send_message_length", self.MAX_GRPC_MESSAGE_LENGTH),
        ]

    @property
    def RUNWAY_API_BASE_URL(self) -> str:
        return f"{self.RUNWAY_API_PROTOCOL}://{self.RUNWAY_API_SERVER_URL}/{self.RUNWAY_API_VERSION}/{self.RUNWAY_API_PREFIX}"

    @property
    def RUNWAY_API_BASE_WORKSPACE_URL(self) -> str:
        return f"{self.RUNWAY_API_BASE_URL}/workspaces/{self.RUNWAY_WORKSPACE_ID}"

    @property
    def RUNWAY_API_BASE_PROJECT_URL(self) -> str:
        return f"{self.RUNWAY_API_BASE_WORKSPACE_URL}/projects/{self.RUNWAY_PROJECT_ID}"

    @property
    def RUNWAY_API_BASE_DATA_SNAPSHOT_URL(self) -> str:
        return f"{self.RUNWAY_API_BASE_PROJECT_URL}/data-snapshots"

    @property
    def RUNWAY_WEBDAV_URL(self) -> str:
        return f"{self.RUNWAY_API_PROTOCOL}://webdav.{'.'.join(self.RUNWAY_API_SERVER_URL.split('.')[1:])}"  # type: ignore[union-attr]


settings = SystemSettings()
