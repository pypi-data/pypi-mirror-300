from field_manager_api.locations.models import Location
from pydantic import BaseModel
from typing import Callable
from uuid import UUID
from field_manager_api.config.config import DATA_URL
from field_manager_api.config.request_handler import get_request_handler


class Project(BaseModel):
    project_id: UUID
    external_id: str
    height_reference: str
    name: str
    organization_id: UUID
    project_id: UUID
    srid: int

    _locations: list["Location"] | None = None
    headers: dict

    @property
    def locations(self) -> list["Location"]:
        if self._locations is None:
            self.fetch_and_set_locations(headers=self.headers)
        return self._locations

    def fetch_and_set_locations(self, headers: dict):
        """Fetch and set locations for the project"""
        url = f"{DATA_URL}/projects/{self.project_id}/locations"
        request_handler = get_request_handler
        locations_data = request_handler(url=url, headers=headers)
        self._locations = [Location(**loc, headers=headers) for loc in locations_data]


def get_projects_request(headers: dict, request_handler: Callable) -> list[Project]:
    """Get projects request"""
    url = f"{DATA_URL}/projects"
    return request_handler(url=url, headers=headers)
