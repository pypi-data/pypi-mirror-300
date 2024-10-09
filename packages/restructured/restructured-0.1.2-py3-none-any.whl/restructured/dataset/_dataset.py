from typing import Any
from typing import Dict
from typing import List
from typing import Literal
from typing import Optional

from restructured._generated.openapi_client import ApiClient  # type: ignore
from restructured._generated.openapi_client import DatasetApi  # type: ignore
from restructured._utils.client import get_client

ParserSetting = Literal["fast", "accurate"]
INTERNAL_FIELDS = ["_datapoint_id", "_kolena_data_type"]


def _process_datapoints(datapoints: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    processed_datapoints = [
        {
            k: v.get("value") if isinstance(v, dict) else v
            for k, v in dp.items()
            if k not in INTERNAL_FIELDS
        }
        for dp in datapoints
    ]

    return processed_datapoints


def upload_datapoints(
    dataset_id: int,
    file_paths: List[str],
    parser_setting: ParserSetting = "fast",
    client: Optional[ApiClient] = None,
) -> None:
    """
    Uploads datapoints to a dataset.

    Args:
        dataset_id (int): The ID of the dataset to upload to.
        file_paths (List[str]): The paths to the files to upload.
        parser_setting (ParserSetting, optional): Possible values are "fast" and "accurate".
        client (Optional[ApiClient], optional): The client to use. Defaults to None.
    """
    if client is None:
        client = get_client()
    api_instance = DatasetApi(client)
    api_instance.add_datapoints_api_v1_dataset_dataset_id_add_put(
        dataset_id, file_paths, parser_setting
    )


def download_dataset(
    dataset_id: int,
    client: Optional[ApiClient] = None,
) -> List[Dict[str, Any]]:
    """
    Downloads a dataset.

    Args:
        dataset_id (int): The ID of the dataset to download.
        client (Optional[ApiClient], optional): The client to use. Defaults to None.

    Returns:
        dataset (List[Dict[str, Any]]): The downloaded dataset.
    """
    if client is None:
        client = get_client()
    api_instance = DatasetApi(client)
    response = api_instance.get_api_v1_dataset_dataset_id_get(
        dataset_id, truncate_content=False
    )
    return _process_datapoints(response.datapoints)
