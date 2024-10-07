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
from typing import Any, Dict, List, Optional

from runway.common.utils import save_settings_to_dotenv
from runway.model_registry.api_client import (
    fetch_model_registry,
    fetch_model_registry_list,
)
from runway.model_registry.schemas import ModelRegistryInfo
from runway.settings import settings


def get_model_registry_list(
    params: Optional[Dict[str, Any]] = None,
) -> List[ModelRegistryInfo]:
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError(
            "RUNWAY_SDK_TOKEN is not set. Please login first.",
        )
    if not settings.RUNWAY_WORKSPACE_ID:
        raise ValueError(
            "RUNWAY_WORKSPACE_ID is not set. Please call set_joined_workspace() first.",
        )
    if not settings.RUNWAY_PROJECT_ID:
        raise ValueError(
            "RUNWAY_PROJECT_ID is not set. Please call set_joined_project() first.",
        )
    model_registries = fetch_model_registry_list(params)
    return [ModelRegistryInfo(**model_registry) for model_registry in model_registries]


def set_model_registry(model_registry_id: int) -> None:
    if not settings.RUNWAY_SDK_TOKEN:
        raise ValueError(
            "RUNWAY_SDK_TOKEN is not set. Please login first.",
        )
    if not settings.RUNWAY_WORKSPACE_ID:
        raise ValueError(
            "RUNWAY_WORKSPACE_ID is not set. Please call set_joined_workspace() first.",
        )
    if not settings.RUNWAY_PROJECT_ID:
        raise ValueError(
            "RUNWAY_PROJECT_ID is not set. Please call set_joined_project() first.",
        )
    model_registry = fetch_model_registry(model_registry_id)

    settings.RUNWAY_MODEL_REGISTRY = str(model_registry)
    os.environ["RUNWAY_MODEL_REGISTRY"] = str(model_registry)

    save_settings_to_dotenv()
