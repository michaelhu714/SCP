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
    return tracks

def plot_orbits_plotly(tracks):
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

    return globe

def plot_orbits_globe_plotly(tracks):
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

    return globe