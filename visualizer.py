import plotly.graph_objects as go 
from skyfield.api import load, wgs84
from tle_downloader import fetch_tle
from datetime import timedelta, datetime
import numpy as np

import plotly.graph_objects as go 
from skyfield.api import load, wgs84
from tle_downloader import fetch_tle
from datetime import timedelta

def get_ground_tracks(satellites, hours=1, interval_minutes=10):
    """
    Compute ground tracks (lat, lon) for each satellite over time.
    Returns: {name: {"lats": [...], "lons": [...]}}
    """
    ts = load.timescale()
    now = ts.now()
    times = [ts.utc((now.utc_datetime() + timedelta(minutes=m))) for m in range(0, hours * 60 + 1, interval_minutes)]

    tracks = {}
    for name, sat in satellites.items():
        lats, lons = [], []
        for time_stamp in times:
            
            subpoint = wgs84.subpoint(sat.at(time_stamp))
            lats.append(subpoint.latitude.degrees)
            lons.append(subpoint.longitude.degrees)
        
        tracks[name] = {"lats": lats, "lons": lons}

    current_positions = {}

    for name, sat in satellites.items():
        ...
        # Add current position
        subpoint_now = wgs84.subpoint(sat.at(ts.now()))
        current_positions[name] = {
            "lat": subpoint_now.latitude.degrees,
            "lon": subpoint_now.longitude.degrees,
        }
    return tracks, current_positions

def plot_orbits_plotly(tracks, current_positions=None, projection_type="equirectangular"):
    """
    Plot ground tracks using Plotly (returns a go.Figure object).
    """
    globe = go.Figure()

    # add orbits 
    for name, track in tracks.items():
        globe.add_trace(go.Scattergeo(
            lon=track["lons"],
            lat=track["lats"],
            mode="lines",
            name=name,
            line=dict(width=2)
        )) 
    
     # Map styling
    globe.update_layout(
        title="Satellite Ground Tracks",
        geo=dict(
            projection_type="equirectangular",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(200, 200, 200)",
            coastlinecolor="black",
            showocean=True,
            oceancolor="lightblue"
        ),
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        height=600,
    )

    if current_positions:
        for name, pos in current_positions.items():
            globe.add_trace(go.Scattergeo(
                lon=[pos["lon"]],
                lat=[pos["lat"]],
                mode="markers",
                marker=dict(size=6, color="red"),
                name=f"{name} (now)"
            )) 

    globe.update_layout(
        title="Satellite Ground Tracks (Flat Map)",
        geo=dict(
            projection_type=projection_type,  # <-- make the projection dynamic
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(200, 200, 200)",
            coastlinecolor="black",
            showocean=True,
            oceancolor="lightblue"
        ),
        margin={"r": 10, "t": 30, "l": 10, "b": 10},
        height=600,
    )

    return globe

def plot_orbits_globe_plotly(tracks, current_positions=None, projection_type="equirectangular"):
    """
    Plot ground tracks on a 3D globe using Plotly (orthographic projection).
    Returns: go.Figure
    """
    globe = go.Figure()

    for name, track in tracks.items():
        globe.add_trace(go.Scattergeo(
            lon=track["lons"],
            lat=track["lats"],
            mode="lines",
            name=name,
            line=dict(width=2),
            showlegend=True
        ))

    globe.update_geos(
        projection_type="orthographic",   
        showland=True, landcolor="rgb(230, 230, 230)",
        showocean=True, oceancolor="lightblue",
        showcoastlines=True, coastlinecolor="black",
        showcountries=True, countrycolor="gray",
    )

    globe.update_layout(
    title="Satellite Ground Tracks (3D Globe)",
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
    height=700,
)

    if current_positions:
        for name, pos in current_positions.items():
            globe.add_trace(go.Scattergeo(
                lon=[pos["lon"]],
                lat=[pos["lat"]],
                mode="markers",
                marker=dict(size=6, color="red"),
                name=f"{name} (now)"
            )) 
        
    globe.update_geos(
        projection_type=projection_type,  # <-- Here's the switch
        
        showland=True, landcolor="rgb(230, 230, 230)",
        showocean=True, oceancolor="lightblue",
        showcoastlines=True, coastlinecolor="black",
        showcountries=True, countrycolor="gray",
    )

    globe.update_layout(
        title="Satellite Ground Tracks (3D Globe)",
        margin={"r": 0, "t": 30, "l": 0, "b": 0},
        height=700,
    )
    

    return globe

def plot_orbit_animation(tracks, projection_type="orthographic"):

    globe = go.Figure()
    names = list(tracks.keys())
    steps = len(list(tracks.values())[0]["lats"])

    # Initial frame (index 0)
    for name in names:
        globe.add_trace(go.Scattergeo(
            lon=[tracks[name]["lons"][0]],
            lat=[tracks[name]["lats"][0]],
            mode="markers+text",
            name=name,
            text=[name],
            marker=dict(size=6),
            showlegend=False
        ))

    # Generate frames with trails
    frames = []
    for i in range(1, steps):
        frame_data = []
        for name in names:
            # Trail: from start up to current frame
            trail_lons = tracks[name]["lons"][:i+1]
            trail_lats = tracks[name]["lats"][:i+1]

            # Add trail line
            frame_data.append(go.Scattergeo(
                lon=trail_lons,
                lat=trail_lats,
                mode="lines",
                line=dict(width=1.5, color="gray"),
                showlegend=False
            ))

            # Add current position marker
            frame_data.append(go.Scattergeo(
                lon=[trail_lons[-1]],
                lat=[trail_lats[-1]],
                mode="markers+text",
                marker=dict(size=6, color="red"),
                text=[name],
                showlegend=False
            ))

        frames.append(go.Frame(data=frame_data, name=str(i)))

    globe.frames = frames

    globe.update_layout(
        title="Animated Satellite Positions (with Trails)",
        geo=dict(
            projection_type=projection_type,
            showland=True,
            landcolor="lightgray",
            showocean=True,
            oceancolor="lightblue",
            coastlinecolor="black",
        ),
        updatemenus=[dict(
            type="buttons",
            showactive=False,
            buttons=[
                dict(label="Play", method="animate", args=[None]),
                dict(label="Pause", method="animate", args=[[None], {"mode": "immediate", "frame": {"duration": 0}, "transition": {"duration": 0}}])
            ]
        )],
        sliders=[dict(
            steps=[dict(method="animate", args=[[str(i)]], label=f"{i}") for i in range(1, steps)],
            transition=dict(duration=0),
            x=0, y=0, len=1.0
        )],
        height=700,
        margin=dict(r=0, l=0, t=30, b=0)
    )

    return globe

def get_ground_tracks(satellites, hours=1, interval_minutes=10):
    ts = load.timescale()
    now = ts.now()
    times = [ts.utc((now.utc_datetime() + timedelta(minutes=m))) for m in range(0, hours * 60 + 1, interval_minutes)]

    tracks = {}
    for name, sat in satellites.items():
        lats, lons = [], []
        for time_stamp in times:
            subpoint = wgs84.subpoint(sat.at(time_stamp))
            lats.append(subpoint.latitude.degrees)
            lons.append(subpoint.longitude.degrees)
        tracks[name] = {"lats": lats, "lons": lons}

    current_positions = {}
    for name, sat in satellites.items():
        subpoint_now = wgs84.subpoint(sat.at(ts.now()))
        current_positions[name] = {
            "lat": subpoint_now.latitude.degrees,
            "lon": subpoint_now.longitude.degrees,
        }
    return tracks, current_positions

def latlon_to_cartesian(lat, lon, alt_km=0, radius=1.0):
    r = radius + alt_km / 6371.0
    lat_rad = np.radians(lat)
    lon_rad = np.radians(lon)
    x = r * np.cos(lat_rad) * np.cos(lon_rad)
    y = r * np.cos(lat_rad) * np.sin(lon_rad)
    z = r * np.sin(lat_rad)
    return x, y, z

def create_earth_sphere(radius=1.0, resolution=100):
    theta = np.linspace(0, 2 * np.pi, resolution)
    phi = np.linspace(0, np.pi, resolution)
    theta, phi = np.meshgrid(theta, phi)
    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)
    return go.Surface(
        x=x, y=y, z=z,
        colorscale=[[0, 'blue'], [1, 'blue']],
        opacity=0.3,
        showscale=False,
        name='Earth'
    )

def plot_orbits_3d_globe(satellites, ts, radius=1.0):
    fig = go.Figure()
    fig.add_trace(generate_starfield(num_stars=1000, radius=2.5))
    fig.add_trace(create_earth_sphere(radius=radius))

    now = ts.now()
    for name, sat in satellites.items():
        subpoint = wgs84.subpoint(sat.at(now))
        x, y, z = latlon_to_cartesian(subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.km, radius)
        fig.add_trace(go.Scatter3d(
            x=[x], y=[y], z=[z],
            mode='markers+text',
            marker=dict(size=5, color='red'),
            text=[name],
            name=name
        ))

    fig.update_layout(
        scene=dict(
            xaxis=dict(showbackground=False),
            yaxis=dict(showbackground=False),
            zaxis=dict(showbackground=False),
            aspectmode='data'
        ),
        margin=dict(r=0, l=0, b=0, t=30),
        title='3D Globe View with Satellites'
    )
    return fig

def generate_starfield(num_stars=500, radius=1.5):
    np.random.seed(42)
    phi = np.random.uniform(0, 2 * np.pi, num_stars)
    costheta = np.random.uniform(-1, 1, num_stars)
    theta = np.arccos(costheta)

    x = radius * np.sin(theta) * np.cos(phi)
    y = radius * np.sin(theta) * np.sin(phi)
    z = radius * costheta

    sizes = np.random.uniform(1, 3, num_stars)
    brightness = np.random.uniform(0.2, 1, num_stars)
    colors = [f"rgba(255, 255, 255, {b:.2f})" for b in brightness]

    return go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=sizes,
            color=colors,
            opacity=1.0
        ),
        hoverinfo='skip',
        showlegend=False
    )
