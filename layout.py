# from dash import html, dcc
# import dash_bootstrap_components as dbc

# # Off-canvas sidebar for controls
# sidebar = dbc.Offcanvas(
#     [
#         html.H5("Controls", className="offcanvas-title"),
#         html.Hr(),

#         html.Label("Number of Satellites"),
#         dcc.Slider(id="num-sats", min=3, max=15, step=1, value=10,
#                    marks={i: str(i) for i in range(3, 16)}),

#         html.Label("Prediction Window (hrs)"),
#         dcc.Slider(id="hours", min=1, max=24, step=1, value=1,
#                    marks={i: str(i) for i in range(1, 25)}),

#         dcc.Checklist(
#             id="options",
#             options=[
#                 {"label": "Check for Close Approaches", "value": "check"},
#                 {"label": "Plot Orbits", "value": "plot"},
#                 {"label": "Use 3D Globe View", "value": "globe"},
#                 {"label": "Live Update", "value": "live"}
#             ],
#             value=["plot"]
#         ),

#         html.Label("Close Approach Threshold (km)"),
#         dcc.Slider(id="threshold", min=1, max=1000, step=1, value=2,
#                    marks={i: str(i) for i in range(0, 1001, 200)})
#     ],
#     id="sidebar",
#     title="Satellite Controls",
#     placement="start",
#     is_open=False,
# )

# # Main layout
# layout = dbc.Container([
#     dbc.Navbar(
#         dbc.Container([
#             dbc.NavbarBrand("Live Satellite Tracker", className="ms-2"),
#             dbc.Button("☰ Controls", id="sidebar-toggle", n_clicks=0, color="primary"),
#         ]),
#         color="dark",
#         dark=True
#     ),

#     sidebar,

#     dcc.Graph(
#         id="live-globe",
#         config={"displayModeBar": True},
#         style={"height": "92vh", "backgroundColor": "black"}
#     ),

#     dcc.Interval(id="interval-component", interval=10000, n_intervals=0),
# ], fluid=True)

from dash import html, dcc

layout = html.Div([
    html.H1("Live Satellite Tracker", style={"textAlign": "center"}),

    dcc.Store(id="satellite-data"),

    dcc.Graph(id="live-globe", style={"height": "95vh"}),

    dcc.Interval(id="interval-component", interval=5000, n_intervals=0)  # 5 sec update
])