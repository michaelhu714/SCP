from dash import html, dcc

layout = html.Div([
    html.H1("Satellite Collision Predictor", style={"textAlign": "center"}),

    html.Div([
        html.Label("Number of Satellites"),
        dcc.Slider(id="num-sats", min=3, max=15, step=1, value=10,
                   marks={i: str(i) for i in range(3, 16)}),

        html.Label("Prediction Window (hrs)"),
        dcc.Slider(id="hours", min=1, max=24, step=1, value=1,
                   marks={i: str(i) for i in range(1, 25)}),

        dcc.Checklist(
            id="options",
            options=[
                {"label": "Check for Close Approaches", "value": "check"},
                {"label": "Plot Orbits", "value": "plot"},
                {"label": "Use 3D Globe View", "value": "globe"},
                {"label": "Live Update", "value": "live"}
            ],
            value=["plot"]
        ),

        html.Label("Close Approach Threshold (km)"),
        dcc.Slider(id="threshold", min=1, max=1000, step=1, value=2,
                   marks={i: str(i) for i in range(0, 1001, 200)})
    ], style={"width": "25%", "float": "left", "padding": "20px"}),

    html.Div([
        dcc.Graph(id="orbit-graph"),
        html.Div(id="warnings")
    ], style={"width": "70%", "float": "right", "padding": "20px"}),

    dcc.Interval(id="interval-component", interval=10000, n_intervals=0)  # update every 10 seconds
])

