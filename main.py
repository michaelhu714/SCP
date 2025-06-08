import argparse
from tle_downloader import fetch_tle
from orbit_propagator import get_satellite_position
from collision_checker import check_close_approaches
from visualizer import plot_satellite_orbits

def main():   
    parser = argparse.ArgumentParser(description="Satellite Collision Predictor")
    parser.add_argument("-num", type=int, default=10, help="Number of satellites to analyze")
    parser.add_argument("-hours", type=int, default=1, help="Hours to predict ahead")
    parser.add_argument("-check", action="store_true", help="Check for close approaches")
    parser.add_argument("-plot", action="store_true", help="Plot satellite orbits using provided hours")

    args = parser.parse_args()

    print("Fetching TLE data...")
    satellites = fetch_tle()
    selected = {k: satellites[k] for k in list(satellites)[:args.num]}

    if args.check:
        print(f"Checking for close approaches over {args.hours} hour(s)...")
        warnings = check_close_approaches(selected, hours=args.hours)
        if warnings:
            print("\nClose Approaches Found:")
            for t, s1, s2, d in warnings:
                print(f" - Time: {t}, Between: {s1} & {s2}, Distance: {d:.2f} km")
        else:
            print("No close approaches found.")

    if args.plot:
        print(f"Plotting orbits for {args.num} satellites...")
        plot_satellite_orbits(selected, hours=args.hours)

    if not args.check and not args.plot:
        print("No action specified. Use --check or --plot.")

if __name__ == "__main__":
    main()