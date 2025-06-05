from skyfield.api import load, wgs84   
from datetime import datetime
from tle_downloader import fetch_tle

def get_satellite_position(satellite, ts=None):
    """
    Computes the current position (lat, lon, altitude in km) of a satellite.
    """
    if ts is None: 
        ts = load.timescale()
    t = ts.now() # where is the satellite now? 
    geocentric = satellite.at(t)
    subpoint = wgs84.subpoint(geocentric) #geocentric position into a subpoint: Latitude, Longitude, Altitude
    return subpoint.latitude.degrees, subpoint.longitude.degrees, subpoint.elevation.km

if __name__ == "__main__":
    satellites = fetch_tle()
    satellite = satellites["CALSPHERE 1"]  # Example satellite
    lat, lon, alt = get_satellite_position(satellite)
    print(f"ISS Position → Lat: {lat:.2f}, Lon: {lon:.2f}, Alt: {alt:.2f} km")