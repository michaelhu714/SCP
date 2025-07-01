import plotly.graph_objects as go
from skyfield.api import load, wgs84
import numpy as np

def create_earth_sphere(radius=6371, resolution=100):
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

def create_star_field(num_stars=2000, radius=40000):
    phi = np.random.uniform(0, np.pi, num_stars)
    theta = np.random.uniform(0, 2 * np.pi, num_stars)

    x = radius * np.sin(phi) * np.cos(theta)
    y = radius * np.sin(phi) * np.sin(theta)
    z = radius * np.cos(phi)

    stars = go.Scatter3d(
        x=x, y=y, z=z,
        mode='markers',
        marker=dict(
            size=1,
            color='white',
            opacity=0.8
        ),
        showlegend=False,
        name='Stars'
    )
    return stars
