import streamlit as st 
from tle_downloader import fetch_tle
from collision_checker import check_close_approaches
from visualizer import get_ground_tracks, plot_orbits_plotly


# configure page

st.set_page_config(page_title="Satellite Collision Predictor", layout = "wide")
st.title("Satellite Collision Predictor")

# sidebar controls 

num_sats = st.sidebar.slider("Number of satellites", min_value = 3, max_value = 15, value = 10)
hours = st.sidebar.slider("Prediction window (hrs)", min_value = 1, max_value = 24, value = 1)
check_collisions = st.sidebar.toggle("Check for close approaches")
plot_orbits = st.sidebar.toggle("Plot satellite orbits")

# main logic

if st.button("Run Prediction"): 
    st.info("Fetching TLE data and running analysis...")
    all_sats = fetch_tle()
    subset_sats= {k: all_sats[k] for k in list(all_sats)[:num_sats]} 

    if plot_orbits: 
        st.subheader("Ground Track Visualization")
        tracks = get_ground_tracks(subset_sats, hours)
        globe = plot_orbits_plotly(tracks)
        st.plotly_chart(globe, use_container_width=True)
        
    if check_collisions:
        st.subheader("Potential Close Approaches")
        warnings = check_close_approaches(subset_sats, hours=hours)
        if warnings:
            st.write("Detected close approaches:")
            for t, s1, s2, d in warnings:
                st.write(f" Time - {t} | {s1} & {s2} → {d:.2f} km")
        else:
            st.success("No close approaches found ")
        