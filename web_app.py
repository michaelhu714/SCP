import streamlit as st 
from tle_downloader import fetch_tle
from collision_checker import check_close_approaches
from visualizer import get_ground_tracks, plot_orbits_plotly, plot_orbits_globe_plotly


# configure page

st.set_page_config(page_title="Satellite Collision Predictor", layout = "wide")
st.title("Satellite Collision Predictor")

# sidebar controls 

num_sats = st.sidebar.slider("Number of satellites", min_value = 3, max_value = 15, value = 10)
hours = st.sidebar.slider("Prediction window (hrs)", min_value = 1, max_value = 24, value = 1)
check_collisions = st.sidebar.toggle("Check for close approaches")
if check_collisions: 
    threshold_km = st.sidebar.slider("Km threshold for close approaches", min_value = 1, max_value = 1000, value = 2)
plot_orbits = st.sidebar.toggle("Plot satellite orbits")
if plot_orbits: 
    globe_view = st.sidebar.checkbox("Use 3D globe view")

# main logic

if st.button("Run Prediction"): 
    st.info("Fetching TLE data and running analysis...")
    all_sats = fetch_tle()
    subset_sats= {k: all_sats[k] for k in list(all_sats)[:num_sats]} 

    if plot_orbits: 
        st.subheader("Ground Track Visualization")
        tracks, positions = get_ground_tracks(subset_sats, hours=hours)
        if globe_view:
            fig = plot_orbits_globe_plotly(tracks, positions)
        else:
            fig = plot_orbits_plotly(tracks, positions)
        st.plotly_chart(fig, use_container_width=True)
        
    if check_collisions:
        warnings = check_close_approaches(subset_sats, hours=hours, threshold_km=threshold_km)
        if warnings: 
            st.subheader("CLOSE APPROACHES DETECTED: ")
            for t, s1, s2, d, threshold in warnings: 
                st.subheader(f" - Time: {t}, Between: {s1} and {s2}, Distance: {d:.2f} km with close approach threshold of {threshold} km")
        else: 
            st.subheader("NO CLOSE APPRAOCHES DETECTED IN SELECTED WINDOW")
        