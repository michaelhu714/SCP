from skyfield.api import load, wgs84
from tle_downloader import fetch_tle
import numpy as np 
from itertools import combinations # helps generate all unique satellite pairs without repetition
from datetime import timedelta

def compute_distance_km(sat1, sat2, time):
    """
    Computes distance between two satellites at time `t` (in km).
    Returns straight line (Euclidean) distance in km between sat1 and sat2
    """
    p1 = sat1.at(time).position.km
    p2 = sat2.at(time).position.km

    return np.linalg.norm(p1 - p2)

def check_close_approaches(satellites, hours=1, interval_min=10, threshold_km= 1000.0):
    ts = load.timescale()
    now = ts.now()
    # Create a list of future times points intervaled by {interval_min} for {hours}
    times = [ts.utc((now.utc_datetime() + timedelta(minutes=m))) for m in range(0, hours * 60 + 1, interval_min)]
    
    results = []
    names = list(satellites.keys())

    for time_stamp in times: 
        for name1, name2 in combinations(names, 2):
            sat1 = satellites[name1]
            sat2 = satellites[name2]
            dist = compute_distance_km(sat1, sat2, time_stamp)
            if dist < threshold_km:
                results.append((time_stamp.utc_iso(), name1, name2, dist, threshold_km))
    
    return results 

if __name__ == "__main__":
    sats = fetch_tle()

    # 20 for performance
    subset = {k: sats[k] for k in list(sats)[:20]}
    warnings = check_close_approaches(subset)
    if warnings: 
        print("CLOSE APPROACHES DETECTED: ")
        printed = False
        for t, s1, s2, d, threshold in warnings: 
            if not printed: 
                print(f"Current Threshold: {threshold} km")
                printed = True
            print(f" - Time: {t}, Between: {s1} and {s2}, Distance: {d:.2f} km")
    else: 
        print("NO CLOSE APPRAOCHES DETECTED IN SELECTED WINDOW")
