from field_manager_api.config.config import DATA_URL
from .models import Location
from typing import Callable


def get_locations_request(
    headers: dict, project_id: str, request_handler: Callable
) -> list[Location]:
    """
    Get the locations by calling the request handler.
    """
    url = get_locations_url(project_id)
    return request_handler(url=url, headers=headers)


def get_locations_url(project_id: str) -> str:
    """
    Get the locations URL.
    """
    return f"{DATA_URL}/projects/{project_id}/locations"
