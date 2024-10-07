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
import contextlib
import logging
import os
import pickle
import tempfile
from pathlib import Path
from subprocess import PIPE, Popen
from typing import Dict, List, Optional, Union
from uuid import uuid4

import numpy as np
import pandas as pd

from runway.dataset.api_client import (
    internal_create_data_snapshot,
    internal_create_data_snapshot_version,
    sdk_create_data_snapshot,
    sdk_create_data_snapshot_version,
    sdk_get_data_snapshot_by_name,
    sdk_get_data_snapshot_detail,
    sdk_get_data_snapshot_list,
    upload_data_snapshot_and_version,
)
from runway.dataset.schemas import DatasetInfo, DatasetVersionInfo
from runway.dataset.values import DatasetFileType
from runway.model_registry.values import WorkloadType
from runway.settings import settings

logger = logging.getLogger(__name__)


def save_dataset(
    name: str,
    data: Union[pd.DataFrame, np.ndarray],
    file_type: DatasetFileType,
    description: Optional[str] = None,
) -> DatasetInfo:
    """upload tabular dataset to the Runway system

    Parameters
    ----------
    name : str
        name string of the tabular dataset
    data : Union[pd.DataFrame, np.ndarray]
        raw data of the dataset
    file_type : DatasetFileType
        file extension string
    description : Optional[str], optional
        details of the dataset, by default None

    Returns
    -------
    DatasetInfo
        saved dataset information
    """
    if isinstance(data, np.ndarray):
        dataframe = pd.DataFrame(data)
    elif isinstance(data, pd.DataFrame):
        dataframe = data
    else:
        raise ValueError("data is not supported object")

    with tempfile.TemporaryDirectory("w+") as tmp_dir:
        filename = (Path(tmp_dir) / uuid4().hex).with_suffix("." + file_type)
        if file_type == DatasetFileType.csv:
            dataframe.to_csv(filename)
        elif file_type == DatasetFileType.parquet:
            dataframe.to_parquet(filename)
        elif file_type == DatasetFileType.pickle:
            with open(file=filename, mode="wb") as f:
                pickle.dump(obj=data, file=f)
        elif file_type == DatasetFileType.npy:
            np.save(file=filename, arr=data)
        else:
            raise ValueError("file_type is not supported type")

        with open(filename, "rb") as file:
            uploaded = upload_data_snapshot_and_version(
                name,
                file,
                description=description,
            )

    return DatasetInfo(**uploaded["data_snapshot"])


def create_dataset(
    name: str,
    description: Optional[str] = None,
    exist_ok: bool = False,
) -> DatasetInfo:
    """create dataset directory to the Runway system

    Parameters
    ----------
    name : str
        name string of the tabular dataset
    description : Optional[str], optional
        details of the dataset, by default None
    exist_ok : bool
        if True, do not raise Error if dataset already exist

    Returns
    -------
    DatasetInfo
        saved dataset information
    """
    if settings.launch_params is None or settings.launch_params.source is None:
        raise ValueError("There are no launch parameters")

    if description is not None and len(description) > 100:
        raise ValueError("Description must be less than 100 characters")

    response: dict
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        response = sdk_create_data_snapshot(name, description, exist_ok)
        return DatasetInfo(**response)
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        response = internal_create_data_snapshot(name, description, exist_ok)
        return DatasetInfo(**response)
    else:
        raise ValueError(
            "entity name of launch param is set to unsupported workload type",
        )


def create_dataset_version(
    dataset_name: str,
    description: Optional[str] = None,
) -> DatasetVersionInfo:
    """create dataset version to the Runway system

    Parameters
    ----------
    dataset_name : str
        name string of dataset
    description : Optional[str], optional
        details of the dataset, by default None

    Returns
    -------
    DatasetVersionInfo
        upgraded dataset version information
    """
    if settings.launch_params is None or settings.launch_params.source is None:
        raise ValueError("There are no launch parameters")

    if description is not None and len(description) > 100:
        raise ValueError("Description must be less than 100 characters")

    dataset_response: dict
    dataset: dict
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        dataset_response = sdk_get_data_snapshot_by_name(dataset_name)
        dataset = dataset_response.get("data_snapshot", None)
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        dataset_response = internal_create_data_snapshot(dataset_name)
        dataset = dataset_response.get("data_snapshot", None)
    else:
        raise ValueError(
            "entity name of launch param is set to unsupported workload type",
        )

    if dataset is None:
        raise ValueError(f"Dataset '{dataset_name}' does not exist.")
    if dataset.get("id", None) is None:
        raise ValueError("Data snapshot id does not exist.")

    dataset_id: int = dataset["id"]
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        dataset_response = sdk_create_data_snapshot_version(dataset_id, description)
        return DatasetVersionInfo(**dataset_response)
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        dataset_response = internal_create_data_snapshot_version(
            dataset_id,
            description,
        )
        return DatasetVersionInfo(**dataset_response)


def get_dataset_list() -> List[DatasetInfo]:
    """
    Get list of datasets

    Returns
    -------
    List[DatasetInfo]
        list of datasets
    """
    if settings.launch_params is None or settings.launch_params.source is None:
        raise ValueError("There are no launch parameters")

    datasets_response: dict
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        datasets_response = sdk_get_data_snapshot_list()
        datasets = datasets_response.get("data_snapshots", [])
        return [DatasetInfo(**dataset) for dataset in datasets]
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        raise NotImplementedError("Not implemented yet")
    else:
        raise ValueError(
            "entity name of launch param is set to unsupported workload type",
        )


def get_dataset(dataset_id: int) -> Optional[DatasetInfo]:
    """
    Get dataset data by id

    Parameters
    ----------
    dataset_id

    Returns
    -------
    DatasetInfo
        dataset data
    """

    if settings.launch_params is None or settings.launch_params.source is None:
        raise ValueError("There are no launch parameters")

    dataset_response: dict
    if settings.launch_params.source.entityname == WorkloadType.dev_instance:
        dataset_response = sdk_get_data_snapshot_detail(dataset_id)
        dataset: Optional[dict] = dataset_response.get("data_snapshot", None)
        return dataset if dataset is None else DatasetInfo(**dataset)
    elif settings.launch_params.source.entityname == WorkloadType.pipeline:
        raise NotImplementedError("Not implemented yet")
    else:
        raise ValueError(
            "entity name of launch param is set to unsupported workload type",
        )


def mount_dataset() -> None:
    if not settings.RUNWAY_PROJECT_ID:
        raise ValueError(
            "RUNWAY_PROJECT_ID is not set. Please call set_joined_project() first.",
        )

    MOUNT_SYNC_INTERVAL = 5
    DIRS = ["dataset", "dataset-staged"]
    CONFIG_DIR = Path.joinpath(Path.home(), ".config", "rclone")
    CONFIG_FILE = Path.joinpath(CONFIG_DIR, "rclone.conf")

    with contextlib.suppress(FileNotFoundError):
        os.remove(CONFIG_FILE)

    os.makedirs(CONFIG_DIR, exist_ok=True)

    with open(CONFIG_FILE, mode="w", encoding="utf-8") as f:
        for DIR in DIRS:
            f.write(
                f"[runway{DIR.replace('-', '')}]"
                f"\ntype = webdav"
                f"\nurl = {settings.RUNWAY_WEBDAV_URL}/{settings.RUNWAY_PROJECT_DIR}/{DIR}/"
                f"\nbearer_token = {settings.RUNWAY_SDK_TOKEN}"
                "\nvendor = other\n\n",
            )

    for DIR in DIRS:
        MOUNT_POINT = f"/home/jovyan/workspace/{DIR}"
        os.makedirs(MOUNT_POINT, exist_ok=True)

        cmd = (
            f"rclone mount runway{DIR.replace('-', '')}:/ {MOUNT_POINT} "
            f"--dir-cache-time {MOUNT_SYNC_INTERVAL}s --allow-other --daemon"
        ) + (" --read-only" if DIR == "dataset" else "")

        p = Popen(cmd.split(" "), stderr=PIPE)
        _, stderr = p.communicate()
        if p.returncode != 0:
            raise RuntimeError(stderr.decode())
