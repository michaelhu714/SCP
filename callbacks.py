from dash import Input, Output, State, ClientsideFunction
import plotly.graph_objects as go
from skyfield.api import load
from tle_downloader import fetch_tle
from visualizer import create_earth_sphere, create_star_field

ts = load.timescale()

def register_callbacks(app):

    # Build initial figure (can be interval or id-triggered — here I leave your original interval-based)
    @app.callback(
        Output("live-globe", "figure"),
        Input("interval-component", "n_intervals"),
        prevent_initial_call=False
    )
    def build_initial_figure(n):
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
                xaxis=dict(visible=False),
                yaxis=dict(visible=False),
                zaxis=dict(visible=False),
                aspectmode='data',
                camera=dict(eye=dict(x=0.4, y=0.4, z=0.4))
            ),
            showlegend=False,
            paper_bgcolor='black',
            plot_bgcolor='black'
        )

        return fig

    # Satellite position updater
    @app.callback(
        Output("satellite-data", "data"),
        Input("interval-component", "n_intervals")
    )
    def update_satellite_positions(n):
        tle_data = fetch_tle()
        now = ts.now()

        sats = []
        for name, sat in list(tle_data.items())[:10]:
            geocentric = sat.at(now)
            x, y, z = geocentric.position.km
            sats.append(dict(name=name, x=x, y=y, z=z))

        return sats

    # Clientside callback — now with allow_duplicate=True
    app.clientside_callback(
        ClientsideFunction(namespace='clientside', function_name='update_satellites'),
        Output("live-globe", "figure", allow_duplicate=True),
        Input("satellite-data", "data"),
        State("live-globe", "figure"),
        prevent_initial_call = True
    )
