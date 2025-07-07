from dash import Input, Output, State
import plotly.graph_objects as go
from skyfield.api import load, wgs84
from src.tle_downloader import fetch_tle
from src.visualizer import create_earth_sphere, create_star_field
from src.collision_checker import check_close_approaches

# Load timescale once globally
ts = load.timescale()

def register_callbacks(app):

    # Main 3D live globe figure update
    @app.callback(
        Output("live-globe", "figure"),
        Input("interval-component", "n_intervals"),
        State("num-sats", "value")
    )
    def update_satellite_positions(n, num_sats):
        tle_data = fetch_tle()
        now = ts.now()

        fig = go.Figure()
        fig.add_trace(create_earth_sphere())
        fig.add_trace(create_star_field())

        for name, sat in list(tle_data.items())[:num_sats]:
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
                xaxis=dict(showbackground=False, visible=False, showgrid=False, zeroline=False),
                yaxis=dict(showbackground=False, visible=False, showgrid=False, zeroline=False),
                zaxis=dict(showbackground=False, visible=False, showgrid=False, zeroline=False),
                aspectmode='data',
                camera=dict(eye=dict(x=0.3, y=0.3, z=0.3))
            ),
            showlegend=False,
            paper_bgcolor='black',
            plot_bgcolor='black'
        )

        return fig

    # Terminal output updater based on checkbox and collision check
    @app.callback(
        Output("terminal-window", "children"),
        Input("interval-component", "n_intervals"),
        State("check-approaches", "value"),
        State("num-sats", "value")
    )
    def update_terminal_output(n, check_values, num_sats):
        if "check" not in check_values:
            return "Terminal ready..."

        tle_data = fetch_tle()
        subset = {k: tle_data[k] for k in list(tle_data)[:num_sats]}

        warnings = check_close_approaches(subset, hours=1, threshold_km=5)

        if warnings:
            lines = ["[⚠] Close Approaches Detected:"]
            for t, s1, s2, d, thresh in warnings:
                lines.append(f"• {t} — {s1} ↔ {s2} | d = {d:.2f} km")
            return "\n".join(lines)
        else:
            return "No close approaches detected in the next hour."

    # Sidebar toggle
    @app.callback(
        Output("sidebar", "style"),
        Input("toggle-sidebar", "n_clicks"),
        State("sidebar", "style")
    )
    def toggle_sidebar(n_clicks, style):
        if n_clicks and n_clicks % 2 == 1:
            style["display"] = "none"
        else:
            style["display"] = "block"
        return style

    # Show/hide terminal based on checkbox
    @app.callback(
        Output("terminal-window", "style"),
        Input("check-approaches", "value"),
        State("terminal-window", "style")
    )
    def toggle_terminal_visibility(check_values, style):
        if "check" in check_values:
            style["display"] = "block"
        else:
            style["display"] = "none"
        return style

