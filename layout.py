from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([

    # Top Title
    html.H1("Live Satellite Tracker", style={
        "textAlign": "center", 
        "marginBottom": "10px", 
        "color": "#00ffff"
    }),

    # Hidden Data Store
    dcc.Store(id="satellite-data"),
    dcc.Store(id="close-approach-data"),

    # Collapsible Sidebar
    html.Div([
        dbc.Button("⚙️ Settings", id="toggle-sidebar", n_clicks=0, color="primary", style={"margin": "10px"}),
        html.Div(id="sidebar", children=[
            html.Label("Number of Satellites"),
            dcc.Slider(id="num-sats", min=3, max=15, step=1, value=10,
                       marks={i: str(i) for i in range(3, 16)}),
            html.Br(),
            dcc.Checklist(
                id="check-approaches",
                options=[{"label": "Check for Close Approaches", "value": "check"}],
                value=[]
            )
        ], style={"padding": "15px"})
    ], style={"position": "absolute", "top": "20px", "left": "20px", "zIndex": "2", "width": "250px", "background": "#111", "color": "#fff", "borderRadius": "10px"}),

    # Main Live Globe
    dcc.Graph(id="live-globe", style={"height": "95vh"}),

    # Terminal Window (hidden unless enabled)
    html.Div(id="terminal-window", children="Terminal ready...",
             style={
                 "position": "absolute",
                 "bottom": "20px",
                 "left": "20px",
                 "width": "300px",
                 "height": "150px",
                 "backgroundColor": "#111",
                 "color": "#00FF00",
                 "padding": "10px",
                 "fontFamily": "Courier New, monospace",
                 "fontSize": "14px",
                 "overflowY": "auto",
                 "borderRadius": "8px",
                 "boxShadow": "0 0 10px #0f0",
                 "display": "none",  # hidden by default
                 "zIndex": "3"
             }),

    # Interval for live updates
    dcc.Interval(id="interval-component", interval=5000, n_intervals=0)
])
