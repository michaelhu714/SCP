import matplotlib.pyplot as plt
from skyfield.api import load, wgs84
from tle_downloader import fetch_tle
from datetime import timedelta

def plot_satellite_orbits(satellites, hours=1, interval_minutes=10):
    """
    Plots ground tracks of satellite orbits on a 2D lat/lon map.
    """
    ts = load.timescale()
    now = ts.now()
    times = [ts.utc((now.utc_datetime() + timedelta(minutes=m))) for m in range(0, hours * 60 + 1, interval_minutes)]

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.set_title("Satellite Ground Tracks")
    ax.set_xlabel("Longitude (degrees)")
    ax.set_ylabel("Latitude (degrees)")
    ax.set_xlim([-180, 180])
    ax.set_ylim([-90, 90])
    ax.grid(True)

    for name, sat in satellites.items():
        lats = []
        lons = []
        for t in times:
            subpoint = wgs84.subpoint(sat.at(t))
            lats.append(subpoint.latitude.degrees)
            lons.append(subpoint.longitude.degrees)
        ax.plot(lons, lats, label=name)

    ax.legend(fontsize='small', loc='upper right')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    sats = fetch_tle()
    # Limit to first 5 satellites for clarity
    small_set = {k: sats[k] for k in list(sats)[:5]}
    plot_satellite_orbits(small_set)
