import folium
from folium.plugins import HeatMap


class MapHandler:
    def __init__(self, locations, height="300px", width="100%", tiles="OpenTopoMap"):
        """
        Initialize the MapHandler with a list of locations.
        Each location should be a dictionary containing 'lat', 'lon', and optionally 'name', 'depth_base', and 'predictions'.
        """
        self.locations = locations
        figure = folium.Figure(
            width=width, height=height
        )  # Adjust the dimensions as needed
        self.map = folium.Map(
            location=[locations[0].lat, locations[0].lon], zoom_start=18, tiles=tiles
        )
        self.map.add_to(figure)

    def plot_locations(self):
        """Plot markers for each location on the map."""
        for ix, location in enumerate(self.locations):
            folium.Marker(
                location=[location.lat, location.lon],
                tooltip=location.get_html_description(location_ix=ix),
                popup=location.name,
                icon=folium.Icon(icon="asterisk", prefix="fa", color="blue"),
            ).add_to(self.map)
        return self.map

    def add_heatmap(self):
        """Add heatmap layer based on location latitudes, longitudes, and depth_base values."""
        HeatMap(
            data=[[loc.lat, loc.lon, loc.depth_base] for loc in self.locations]
        ).add_to(self.map)
        return self.map

    def check_if_prediction_contains_soil_type(self, predictions):
        """Helper function to determine the color based on soil type in predictions."""
        for prediction in predictions:
            if "quick_clay" in prediction["soil_type"]:
                return "red"
            elif "clay" in prediction["soil_type"]:
                return "yellow"
            else:
                return "green"

    def add_prediction_ring_around_locations(self):
        """Add a colored ring around each location based on soil type in predictions."""
        for location in self.locations:
            predictions = location.predictions
            if predictions:
                color = self.check_if_prediction_contains_soil_type(predictions)
            else:
                color = "green"  # Default to green if no predictions

            folium.Circle(
                location=[location.lat, location.lon],
                radius=20,  # Radius in meters
                color=color,
                fill=False,
            ).add_to(self.map)
        return self.map

    def get_map(self):
        """Return the generated map with all layers."""
        return self.map
