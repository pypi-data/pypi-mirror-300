import re
from field_manager_api.auth.auth import set_bearer_token_header
from field_manager_api.config.request_handler import get_request_handler
from field_manager_api.locations.get_locations import get_locations_request
from field_manager_api.methods import get_methods
from field_manager_api.projects.get_projects import get_projects_request
from field_manager_api.projects.get_projects import Project


class FieldManagerAPI:
    """Field Manager API class"""

    headers: dict

    def __init__(self):
        print("Field Manager API init")

    def set_token(self, token):
        self.headers = set_bearer_token_header(token)
        print("Token set successfully")

    def get_list_of_all_projects(self):
        self.validate_header()
        projects = get_projects_request(self.headers, get_request_handler)
        return projects

    def search_for_project_name(self, substring: str) -> list[str]:
        """Retrieve a list of project names that match the substring using regex."""
        projects = self.get_list_of_all_projects()
        project_names = [project["name"] for project in projects]

        # Compile the regex pattern for case-insensitive matching
        pattern = re.compile(re.escape(substring), re.IGNORECASE)

        matching_project_names = [
            project_name
            for project_name in project_names
            if pattern.search(project_name)
        ]
        return matching_project_names

    def get_project_by_name(self, project_name: str) -> Project:
        """Retrieve a project by its name."""
        projects = self.get_list_of_all_projects()
        for project_json in projects:
            if project_json["name"] == project_name:
                project = Project(**project_json, headers=self.headers)
                return project
        raise ValueError(f"Project with name '{project_name}' not found.")

    def validate_header(self):
        if self.headers is None:
            raise ValueError("Token not set")

    def get_locations(self, project_id: str = None):
        self.validate_header()
        if project_id is None and self.project_id is not None:
            project_id = self.project_id
        locations = get_locations_request(self.headers, project_id, get_request_handler)
        return locations

    def get_methods(self, method_types: list[int] = None):
        methods = get_methods(self.locations, method_types)
        self.methods = methods


#
#
#
#
#    def plot_locations(self):
#        self.m = MapHandler(self.methods)
#        self.m.plot_locations()
#        return self.m.get_map()
#
#    def plot_heatmap(self):
#        self.m.add_heatmap()
#        self.m.add_prediction_ring_around_locations()
#        return self.m.get_map()
#
#    def create_ground_model(self):
#        if self.methods is None:
#            raise ValueError("Methods not set")
#        plotter = Plotter(self.methods)
#        plotter.plot()
#
#    def create_bedrock_model(self):
#        if self.methods is None:
#            raise ValueError("Methods not set")
#        plotter = Plotter(self.methods)
#        plotter.plot_3d_surface_with_layers()
#
#    #def create_datarapport(self):
#    #    if self.methods is None:
#    #        raise ValueError("Methods not set")
#    #    # Example of how to use this class
#
#        # Assuming 'get_methods()' gives a list of Method objects
#
#    #    print("Connecting to ChatGPTAPI..")
#    #    # Create the report class
#    #    report = WordDocReport(self.methods)
#
#    #    # Generate the map and capture a screenshot
#    #    report.add_existing_map(self.m.map)
#    print("Creating datarapport..")
#    report.capture_map_screenshot()

# Create the Word document report
#    report.create_report(
#        description="This report contains geotechnical data and visualizations of sounding locations."
#    )
#    print("Datarapport created successfully")
