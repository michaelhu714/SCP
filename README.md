# 🌍 Satellite Collision Predictor

An interactive Dash app that visualizes real-time satellite positions and detects potential close approaches in Earth orbit.

## Features

- A 3D globe with live-updating satellite markers using Skyfield and TLE data
- Starfield background and smooth camera controls
- Sidebar controls for:
  - Number of satellites displayed
  - Close approach detection window and threshold

## Tech Stack
- Python 3.10+
- Dash & Plotly
- Skyfield
- Bootstrap (for dark theme + sidebar)

## Setup Instructions

```bash
# Clone and enter
git clone https://github.com/michaelhu714/SCP.git
cd SCP

# Set up environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py