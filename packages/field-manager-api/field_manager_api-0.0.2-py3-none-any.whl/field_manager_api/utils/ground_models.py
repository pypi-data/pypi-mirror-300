import random
import plotly.graph_objects as go
import numpy as np
from scipy.interpolate import griddata


class Method:
    def __init__(self, depth_top, depth_base, x, y, z):
        self.depth_top = depth_top
        self.depth_base = depth_base
        self.x = x
        self.y = y
        self.z = z
        self.predictions = self.predict_soil_layers(num_splits=2)

    def predict_soil_layers(
        self, num_splits=2, types=["sand", "clay", "silt", "quick_clay"]
    ):
        split_depth = (self.depth_base - self.depth_top) / num_splits
        current_depth = self.depth_top

        predictions = []
        for _ in range(num_splits):
            next_depth = current_depth + split_depth
            if next_depth > self.depth_base:
                next_depth = self.depth_base

            soil_type = random.choice(types)
            predictions.append(
                {
                    "start": self.z - current_depth,
                    "end": self.z - next_depth,
                    "x": self.x,
                    "y": self.y,
                    "soil_type": soil_type,
                }
            )

            current_depth = next_depth

        return predictions


class Plotter:
    def __init__(self, methods):
        self.methods = methods

    def plot(self):
        fig = go.Figure()
        color_map = {
            "sand": "green",
            "clay": "yellow",
            "silt": "orange",
            "quick_clay": "red",
        }

        for method in self.methods:
            for pred in method.predictions:
                fig.add_trace(
                    go.Scatter3d(
                        x=[pred["x"]],
                        y=[pred["y"]],
                        z=[pred["start"]],
                        mode="markers+text",
                        marker=dict(size=5, color=color_map.get(pred["soil_type"])),
                        text=[f"{pred['soil_type']} ({pred['start']} - {pred['end']})"],
                        textposition="top center",
                    )
                )

                fig.add_trace(
                    go.Scatter3d(
                        x=[pred["x"], pred["x"]],
                        y=[pred["y"], pred["y"]],
                        z=[pred["start"], pred["end"]],
                        mode="lines",
                        line=dict(color=color_map.get(pred["soil_type"]), width=4),
                    )
                )

        fig.update_layout(
            scene=dict(
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                zaxis_title="Height Above Terrain",
            ),
            title="3D Soil Layer Visualization",
            margin=dict(r=10, l=10, b=10, t=50),
        )

        try:
            fig.show()
        except Exception as e:
            print(f"Error displaying plot: {e}")
            fig.write_html("soil_layers_plot.html")
            print("Plot saved as 'soil_layers_plot.html'. Please open it in a browser.")

    def plot_surface_last_depth(self):
        x_coords = [pred["x"] for method in self.methods for pred in method.predictions]
        y_coords = [pred["y"] for method in self.methods for pred in method.predictions]
        z_last = [
            method.z - pred["end"]
            for method in self.methods
            for pred in method.predictions
        ]
        z_top = [method.z for method in self.methods]
        # Create a fine grid for smooth interpolation
        xi = np.linspace(min(x_coords), max(x_coords), 100)
        yi = np.linspace(min(y_coords), max(y_coords), 100)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolate the z values
        zi = griddata((x_coords, y_coords), z_last, (xi, yi), method="cubic")

        # Create the surface plot
        fig = go.Figure(
            data=[
                go.Surface(
                    z=zi,
                    x=xi,
                    y=yi,
                    colorscale="Viridis",
                    colorbar_title="Last Depth Above Terrain",
                    showscale=True,
                )
            ]
        )

        # Add scatter points for the original data
        fig.add_trace(
            go.Scatter3d(
                x=x_coords,
                y=y_coords,
                z=z_top,
                mode="markers",
                marker=dict(size=5, color=z_top, colorscale="Viridis", showscale=False),
                name="Original Data Points",
            )
        )

        fig.update_layout(
            scene=dict(
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                zaxis_title="Height Above Terrain",
                aspectratio=dict(x=1, y=1, z=0.5),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            ),
            title="Surface Plot of Last Depth",
            margin=dict(r=10, l=10, b=10, t=50),
        )

        try:
            fig.show()
        except Exception as e:
            print(f"Error displaying plot: {e}")
            fig.write_html("last_depth_surface_plot.html")
            print(
                "Plot saved as 'last_depth_surface_plot.html'. Please open it in a browser."
            )

    def plot_last_depth_contour(self):
        x_coords = [pred["x"] for method in self.methods for pred in method.predictions]
        y_coords = [pred["y"] for method in self.methods for pred in method.predictions]
        z_last = [pred["end"] for method in self.methods for pred in method.predictions]

        # Create a fine grid for smooth interpolation
        xi = np.linspace(min(x_coords), max(x_coords), 100)
        yi = np.linspace(min(y_coords), max(y_coords), 100)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolate the z values
        zi = griddata((x_coords, y_coords), z_last, (xi, yi), method="cubic")

        # Create the contour plot
        fig = go.Figure(
            data=[
                go.Contour(
                    z=zi,
                    x=xi[0],
                    y=yi[:, 0],
                    colorscale="Viridis",
                    colorbar_title="Last Depth Above Terrain",
                    contours=dict(
                        showlabels=True, labelfont=dict(size=12, color="white")
                    ),
                )
            ]
        )

        # Add scatter points for the original data
        fig.add_trace(
            go.Scatter(
                x=x_coords,
                y=y_coords,
                mode="markers",
                marker=dict(
                    size=10, color=z_last, colorscale="Viridis", showscale=False
                ),
                text=[f"Depth: {z:.2f}" for z in z_last],
                hoverinfo="text",
                name="Original Data Points",
            )
        )

        fig.update_layout(
            xaxis_title="X Coordinate",
            yaxis_title="Y Coordinate",
            title="Contour Plot of Last Depth",
            margin=dict(r=10, l=10, b=10, t=50),
        )

        try:
            fig.show()
        except Exception as e:
            print(f"Error displaying plot: {e}")
            fig.write_html("last_depth_contour_plot.html")
            print(
                "Plot saved as 'last_depth_contour_plot.html'. Please open it in a browser."
            )

    def plot_3d_surface(self):
        # Extract x, y, and z (last depth) from methods
        x = [method.x for method in self.methods]
        y = [method.y for method in self.methods]
        z = [
            method.z - method.depth_base for method in self.methods
        ]  # Last depth relative to terrain

        # Create a fine grid for smooth interpolation
        xi = np.linspace(min(x), max(x), 100)
        yi = np.linspace(min(y), max(y), 100)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolate the z values
        zi = griddata((x, y), z, (xi, yi), method="cubic")

        # Create the 3D surface plot
        fig = go.Figure(
            data=[
                go.Surface(
                    z=zi,
                    x=xi,
                    y=yi,
                    colorscale="Viridis",
                    colorbar_title="Depth Below Terrain",
                )
            ]
        )

        # Add scatter points for the original data
        fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=dict(size=5, color=z, colorscale="Viridis", showscale=False),
                name="Original Data Points",
            )
        )

        # Update the layout for better visualization
        fig.update_layout(
            title="3D Surface Plot of Soil Depth",
            scene=dict(
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                zaxis_title="Depth Below Terrain",
                aspectratio=dict(x=1, y=1, z=0.5),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            ),
            margin=dict(r=20, l=10, b=10, t=50),
        )

        try:
            fig.show()
        except Exception as e:
            print(f"Error displaying plot: {e}")
            fig.write_html("3d_surface_plot.html")
            print("Plot saved as '3d_surface_plot.html'. Please open it in a browser.")

    def plot_3d_surface_with_layers(self):
        # Extract x, y, and z (last depth) from methods
        x = [method.x for method in self.methods]
        y = [method.y for method in self.methods]
        z = [
            method.z - method.depth_base for method in self.methods
        ]  # Last depth relative to terrain

        # Create a fine grid for smooth interpolation
        xi = np.linspace(min(x), max(x), 100)
        yi = np.linspace(min(y), max(y), 100)
        xi, yi = np.meshgrid(xi, yi)

        # Interpolate the z values
        zi = griddata((x, y), z, (xi, yi), method="cubic")

        # Create the 3D surface plot
        fig = go.Figure(
            data=[
                go.Surface(
                    z=zi,
                    x=xi,
                    y=yi,
                    colorscale="Viridis",
                    colorbar_title="Depth Below Terrain",
                    opacity=0.8,  # Make the surface slightly transparent
                )
            ]
        )

        # Add scatter points for the original data
        fig.add_trace(
            go.Scatter3d(
                x=x,
                y=y,
                z=z,
                mode="markers",
                marker=dict(size=5, color=z, colorscale="Viridis", showscale=False),
                name="Original Data Points",
            )
        )

        # Color map for soil types
        color_map = {
            "sand": "green",
            "clay": "yellow",
            "silt": "orange",
            "quick_clay": "red",
        }

        # Add vertical lines for each soil layer prediction
        for method in self.methods:
            for pred in method.predictions:
                fig.add_trace(
                    go.Scatter3d(
                        x=[pred["x"]],
                        y=[pred["y"]],
                        z=[pred["start"]],
                        mode="markers+text",
                        marker=dict(size=5, color=color_map.get(pred["soil_type"])),
                        text=[f"{pred['soil_type']} ({pred['start']} - {pred['end']})"],
                        textposition="top center",
                    )
                )

                fig.add_trace(
                    go.Scatter3d(
                        x=[pred["x"], pred["x"]],
                        y=[pred["y"], pred["y"]],
                        z=[pred["start"], pred["end"]],
                        mode="lines",
                        line=dict(color=color_map.get(pred["soil_type"]), width=4),
                    )
                )
        # for method in self.methods:
        #     for pred in method.predictions:
        #         fig.add_trace(go.Scatter3d(
        #             x=[method.x, method.x],
        #             y=[method.y, method.y],
        #             z=[method.z, method.z - method.depth_base],
        #             mode='lines',
        #             line=dict(color=color_map.get(pred['soil_type'], 'gray'), width=5),
        #             name=f"{pred['soil_type']} ({pred['start']} - {pred['end']})"
        #         ))

        # Update the layout for better visualization
        fig.update_layout(
            title="3D Surface Plot of Soil Depth with Layer Predictions",
            scene=dict(
                xaxis_title="X Coordinate",
                yaxis_title="Y Coordinate",
                zaxis_title="Depth Below Terrain",
                aspectratio=dict(x=1, y=1, z=0),
                camera=dict(eye=dict(x=1.5, y=1.5, z=1.2)),
            ),
            margin=dict(r=20, l=10, b=10, t=50),
        )

        try:
            fig.show()
        except Exception as e:
            print(f"Error displaying plot: {e}")
            fig.write_html("3d_surface_plot_with_layers.html")
            print(
                "Plot saved as '3d_surface_plot_with_layers.html'. Please open it in a browser."
            )


# # Example usage
# methods = [
#     Method(depth_top=0, depth_base=35, x=1, y=2, z=51),
#     Method(depth_top=0, depth_base=33, x=5, y=5, z=52),
#     Method(depth_top=0, depth_base=30, x=2, y=2, z=50),
#     Method(depth_top=0, depth_base=30, x=5, y=10, z=49),
#     Method(depth_top=0, depth_base=30, x=15, y=20, z=55),
# ]


# plotter = Plotter(methods)
# plotter.plot()
# plotter.plot_surface_last_depth()
# plotter.plot_last_depth_contour()
# plotter.plot_3d_surface_with_layers()
