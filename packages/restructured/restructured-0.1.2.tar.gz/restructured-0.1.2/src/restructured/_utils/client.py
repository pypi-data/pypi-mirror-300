from importlib.metadata import version
from typing import Optional

from restructured._generated.openapi_client import ApiClient  # type: ignore
from restructured._generated.openapi_client import Configuration  # type: ignore
from restructured._utils.config import get_api_key
from restructured._utils.config import get_host

RESTRUCTURED_VERSION = version("restructured")


def get_client(
    api_key: Optional[str] = None,
    host: Optional[str] = None,
) -> ApiClient:
    if api_key is None:
        api_key = get_api_key()
    if host is None:
        host = get_host()

    if api_key is None:
        raise ValueError("No API token provided")

    configuration = Configuration(
        host=host,
        api_key={"APIKeyHeader": api_key},
    )
    client = ApiClient(configuration)
    client.user_agent = f"restructured-python-{RESTRUCTURED_VERSION}"
    return client
