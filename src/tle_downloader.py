from skyfield.api import load

def fetch_tle(category_url="https://celestrak.org/NORAD/elements/gp.php?GROUP=active&FORMAT=tle"):
    """
    Fetches TLE data from Celestrak for active satellites.
    Returns a dictionary of satellite names and Skyfield EarthSatellite objects.
    """
    satellites = load.tle_file(category_url)
    print(f"Loaded {len(satellites)} satellites")
    return {sat.name: sat for sat in satellites}

if __name__ == "__main__":
    sats = fetch_tle()
    for name in list(sats.keys())[:5]:  # Print first 5 satellite names
        print(name)