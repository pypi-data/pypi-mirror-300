from field_manager_api.config.request_handler import get_request_handler
from field_manager_api.methods.models import Method
from pydantic import BaseModel, root_validator
from pyproj import Transformer
from field_manager_api.config.config import DATA_URL
from uuid import UUID


class Location(BaseModel):
    project_id: UUID
    location_id: UUID
    name: str
    point_easting: float | None = None
    point_northing: float | None = None
    point_z: float | None = None
    project_id: str
    srid: int

    lat: float | None = None
    lon: float | None = None

    _methods: list["Method"] | None = None

    headers: dict | None = None

    @property
    def methods(self) -> list["Method"]:
        if self._methods is None:
            self.fetch_and_set_methods(headers=self.headers)
        return self._methods

    def __str__(self) -> str:
        """Return a short description with a summary of the number of methods per type as a plain text."""
        desc = f"Location: {self.name}\nMethods:\n"

        # Count methods by type
        num_methods_by_types = {}
        for method in self.methods:
            if method.method_type.name in num_methods_by_types:
                num_methods_by_types[method.method_type.name] += 1
            else:
                num_methods_by_types[method.method_type.name] = 1

        # Add each method type with its count
        for name, num in num_methods_by_types.items():
            desc += f"- {name}: {num}\n"
        return desc

    def get_html_description(self, location_ix) -> str:
        """Return a long description with an ordered list of methods starting at 0."""
        desc = f"<b>Location:</b><br>Name: {self.name}<br>Index: {location_ix}<br><br>Methods:<br><ol start='0'>"

        # Add each method as a numbered item in the list
        for idx, method in enumerate(self.methods):
            desc += f"<li>{method.method_type.name}</li>"

        desc += "</ol>"
        return desc

    def fetch_and_set_methods(self, headers: dict):
        """Fetch and set methods for the location"""

        url = f"{DATA_URL}/projects/{self.project_id}/locations/{self.location_id}/methods"
        request_handler = get_request_handler
        methods = request_handler(url=url, headers=headers)
        self._methods = [
            Method(**method, headers=headers, project_id=self.project_id)
            for method in methods
        ]

    @root_validator(pre=True)
    def set_lat_lon(cls, values):
        # Set lat and lon based on point_x_ and point_y_ fields
        values["lat"], values["lon"] = cls.convert_coordinates(values)
        return values

    @classmethod
    def convert_coordinates(cls, values):
        transformer = Transformer.from_crs(
            f"epsg:{values['srid']}", "epsg:4326", always_xy=True
        )
        lon, lat = transformer.transform(
            values["point_easting"], values["point_northing"]
        )
        return lat, lon
