# layouts/incomplete_layout.py

from dash import html, dcc
import dash_bootstrap_components as dbc
import datetime
import dash_mantine_components as dmc
import dash_iconify


incomplete_layout = dmc.MantineProvider(
    withCssVariables=True,
    children=[
                dmc.Paper(
                    withBorder=False,
                    radius=0,
                    shadow="xs",
                    p="md",
                    style={"backgroundColor": "#1F53C9", "color": "white"},
                    children=dbc.Row(
                        [
                            # Left: title 
                            dbc.Col(
                                dmc.Stack(
                                    gap=2,
                                    children=[
                                        dmc.Text(
                                            id="incomplete-title",
                                            fw=650,     
                                            fz=25,       
                                            style={"color": "white", "margin": 0},
                                        ),
                                        dmc.Text(
                                            "Incomplete pathways represent patients still waiting to start treatment — at any stage of their journey, from diagnostics to consultant appointments or procedures",  # optional subtitle
                                            c="rgba(255,255,255,0.85)",
                                            fz="sm",
                                        ),
                                    ],
                                ),
                                width="auto",
                            ),

                            # Right: buttons 
                            dbc.Col(
                                html.Div(
                                    [
                                        dbc.Button(
                                            dash_iconify.DashIconify(icon="mdi:home-circle", width=26, color="white"),
                                            id="back-home-btn",
                                            title="Go back to Home Page",
                                            color="light",
                                            style={
                                                "background": "transparent",
                                                "color": "white",
                                                "border": "1px solid rgba(255,255,255,0.6)",
                                                "boxShadow": "0 1px 3px rgba(0,0,0,0.1)",
                                            },
                                            n_clicks=0,
                                        ),
                                        dmc.Button(
                                            leftSection=dash_iconify.DashIconify(
                                                icon="mdi:help-circle-outline", width=20, color="white"
                                            ),
                                            children="Help",
                                            id="help-open-btn-incomplete",
                                            variant="subtle",
                                            size="sm",
                                            styles={
                                                "root": {
                                                    "marginLeft": 8,
                                                    "color": "white",
                                                }
                                            },
                                        ),
                                    ],
                                    style={
                                        "display": "flex",
                                        "justifyContent": "flex-end",
                                        "alignItems": "center",
                                    },
                                ),
                                width="auto",
                                className="ms-auto",
                            ),
                        ],
                        align="center",
                        className="my-0",
                    ),
                ),
        dmc.Space(h=15),  # adds 15px vertical space

        dbc.Container(
            [   
                html.Div(id="dummy-trigger", children=1, style={"display": "none"}),
                dcc.Store(id="incomplete-selected-icb", storage_type="memory"),
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.Label("Select Metric to Display"),
                                html.Div(
                                    [
                                dcc.Dropdown(
                                    id="metric-selector",
                                    options=[
                                        {
                                            "label": "Average (median) waiting time (in weeks)",
                                            "value": "Average (median) waiting time (in weeks)",
                                        },
                                        {
                                            "label": "% within 18 weeks",
                                            "value": "% within 18 weeks",
                                        },
                                        {
                                            "label": "92nd percentile waiting time (in weeks)",
                                            "value": "92nd percentile waiting time (in weeks)",
                                        },
                                        {
                                            "label": "Total number of incomplete pathways",
                                            "value": "Total number of incomplete pathways",
                                        },
                                        {
                                            "label": "Total 52 plus weeks",
                                            "value": "Total 52 plus weeks",
                                        },
                                    ],
                                    value="Average (median) waiting time (in weeks)",
                                    clearable=False,
                                    style={"flex": 1},
                                ),
                                html.Span(id="metric-help-icon-incomplete", style={"marginLeft": "6px"}),
                                    ],
                                    style={"display": "flex", "alignItems": "center"}
                                ),
                            ],
                            md=4,
                        ),
                    ],
                    className="mb-3",
                ),
                dbc.Row([dbc.Col([dcc.Graph(id="incomplete-line-chart")])]),
                html.Hr(),
                dbc.Row(
                    [
                        # LEFT: Bar Chart
                        dbc.Col(
                            [
                                html.H5(
                                    "Monthly Comparison by Treatment Function",
                                    className="mb-4",
                                ),
                                dcc.Graph(
                                    id="bar-chart-comparison",
                                    style={"height": "450px"},
                                ),
                            ],
                            md=8,
                        ),
                        # RIGHT: Sidebar Controls
                        dbc.Col(
                            [
                                html.Label("Select Month"),
                                dmc.MonthPickerInput(
                                    id="month-selector",
                                    value=datetime.date(2024, 3, 1),
                                    minDate=datetime.date(2022, 9, 1),
                                    maxDate=datetime.date(2025, 3, 31),
                                    size="sm",
                                    style={"width": "100%"},
                                ),
                                html.Br(),
                                html.Label("Choose chart mode"),
                                dcc.RadioItems(
                                    id="chart-mode",
                                    options=[],
                                    value="top",
                                    labelStyle={"display": "block"},
                                    className="mb-3",
                                ),
                                html.Div(
                                    id="manual-selection-section",
                                    children=[
                                        html.Label(
                                            "Select up to 5 Treatment Functions"
                                        ),
                                        dmc.MultiSelect(
                                            id="treatment-function-checklist",
                                            data=[],
                                            placeholder="Pick up to 5 functions",
                                            maxValues=5,
                                            searchable=False,
                                            clearable=True,
                                            nothingFoundMessage="No match",
                                            style={"marginBottom": "1rem"},
                                        ),
                                        html.Div(
                                            id="selection-warning",
                                            className="text-danger small mt-1",
                                        ),
                                    ],
                                ),
                                dbc.Button(
                                    "Display Chart",
                                    id="display-chart-btn",
                                    color="primary",
                                    className="mt-2",
                                    n_clicks=0,
                                ),
                            ],
                            md=4,
                            style={
                                "backgroundColor": "#f8f9fa",
                                "padding": "1.25rem",
                                "borderRadius": "0.5rem",
                                "boxShadow": "0 2px 6px rgba(0,0,0,0.05)",
                            },
                        ),
                    ],
                    className="mb-5",
                ),
                html.Hr(),
                html.Div(
                    id="incomplete-imd-block",
                    children=[
                dbc.Row(
                    [
                        dbc.Col(
                            [
                                html.H5("Deprivation and Waiting Times across ICBs",
                                        className="mb-3"),
                                html.H6(id="incomplete-imd-regional-subtitle", className="mb-2"),  
                                html.Div(
                                    id="incomplete-imd-map",
                                    style={
                                        "height": "520px",
                                        "width": "100%",
                                        "background": "#f2f4f7",  
                                        "border": "1px solid #e5e7eb",
                                        "borderRadius": "8px",
                                    },
                                ),
                            ],
                            md=6,
                        ),
                        # RIGHT: ICB RTT bars + clear-selection button
                        dbc.Col(
                            [
                                dcc.Graph(id="incomplete-icb-rtt-bars", style={"height": "460px"}),

                                dbc.Button(
                                    "Clear selection",
                                    id="incomplete-clear-icb-selection",
                                    color="secondary",
                                    outline=True,
                                    size="sm",
                                    className="mt-2",
                                    n_clicks=0,
                                    title="Return to ICB hover mode on the map",
                                ),
                            ],
                            md=6,
                        ),
                    ],
                    className="mb-5",
                ),
                ]),
                # NATIONAL IMD block (hidden unless National granularity)
                html.Div(
                    id="incomplete-national-imd-block",
                    children=[
                        dbc.Row([
                            dbc.Col(
                                [
                                    html.H5("Compare ICBs by Deprivation and Population", className="mb-3"),
                                    html.H6(id = "incomplete-imd-national-subtitle", className="mb-2"),
                                    dcc.Graph(id="incomplete-national-imd-scatter", style={"height": "520px"}),
                                ],
                                md=12,
                            ),
                        ])
                    ],
                    style={"display": "none"},  # hidden by default; toggled by callback
                ),  
                dmc.Drawer(
                    id="help-drawer-incomplete",
                    title=dmc.Text("User Guide", fw=700, fz="lg"),
                    opened=False,
                    position="right",
                    size=420,             
                    overlayProps={"opacity": 0.15, "blur": 1.5},
                    padding="md",
                    children=html.Div(id="help-body-incomplete"),
                ),            
            ],
            fluid=True,
        )
    ],
)

