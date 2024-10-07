from typing import Callable

from field_manager_api.config.config import DATA_URL
from field_manager_api.methods.models import Method


def get_models_request(
    headers: dict, project_id: str, request_handler: Callable
) -> list[Method]:
    """
    Get the locations by calling the request handler.
    """
    url = get_methods_url(project_id)
    return request_handler(url=url, headers=headers)


def get_methods_url(project_id: str) -> str:
    """
    Get the locations URL.
    """
    return f"{DATA_URL}/projects/{project_id}/locations"
