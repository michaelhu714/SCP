#callbacks.py
from dash import Input, Output
import plotly.graph_objects as go
from skyfield.api import load, wgs84
from tle_downloader import fetch_tle
from visualizer import create_earth_sphere, create_star_field

# Load timescale once
ts = load.timescale()

# Callback to update satellite positions

def register_callbacks(app):
    @app.callback(
    Output("sidebar", "is_open"),
    Input("sidebar-toggle", "n_clicks"),
    prevent_initial_call=True
)
    def toggle_sidebar(n):
        return True if n % 2 == 1 else False

    @app.callback(
        Output("live-globe", "figure"),
        Input("interval-component", "n_intervals")
    )
    def update_satellite_positions(n):
        tle_data = fetch_tle()
        now = ts.now()

        fig = go.Figure()
        fig.add_trace(create_earth_sphere())
        fig.add_trace(create_star_field())

        for name, sat in list(tle_data.items())[:10]:
            geocentric = sat.at(now)
            x, y, z = geocentric.position.km

            fig.add_trace(go.Scatter3d(
                x=[x], y=[y], z=[z],
                mode='markers',
                marker=dict(size=4, color='red'),
                name=name
            ))

        fig.update_layout(
            margin=dict(l=0, r=0, t=0, b=0),
            scene=dict(
                xaxis=dict(showbackground=False),
                yaxis=dict(showbackground=False),
                zaxis=dict(showbackground=False),
                aspectmode='data'
            ),
            showlegend=False,
            paper_bgcolor='black',
            plot_bgcolor='black'
        )

        return fig
    

