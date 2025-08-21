# layouts/home_layout.py
from dash import html, dcc
import dash_mantine_components as dmc
import dash_iconify
import dash_bootstrap_components as dbc
import dash_leaflet as dl
from queries import get_all_regions_geojson
from dash_extensions.javascript import assign

# ---- stat card factory (icon + title + big value + caption) ----
def StatCard(title: str, value_id: str, caption: str, icon: str, color: str = "blue"):
    return dmc.Card(
        withBorder=True,
        radius="lg",
        shadow="xs",
        p="md",
        style={"background": "white"},
        children=[
            dmc.Group(
                [
                    dmc.ThemeIcon(
                        dash_iconify.DashIconify(icon=icon, width=20),
                        variant="light",
                        radius="xl",
                        size=36,
                        color=color,
                    ),
                    dmc.Stack(
                        [
                            dmc.Text(title, fw=700, fz="sm"),
                            dmc.Text(caption, size="xs", c="dimmed"),
                        ],
                        gap=0,
                    ),
                ],
                justify="space-between",
            ),
            dmc.Divider(my="sm"),
            dmc.Text(id=value_id, fw=800, fz=28, lh=1.1),  
        ],
    )

nhs_header_card = dmc.Card(
    withBorder=True, radius="lg", shadow="xs", p="md",
    style={
        "background": "linear-gradient(135deg, #f8fbff 0%, #f1f5ff 100%)",
        "borderColor": "#e6eefb",
    },
    children=[
        dmc.Group(
            [
                dmc.ThemeIcon(
                    dash_iconify.DashIconify(icon="mdi:shield-cross-outline", width=22),
                    variant="filled", radius="xl", size=38, color="indigo",
                ),
                dmc.Stack(
                    [
                        dmc.Text("NHS England", fw=800, fz="md"),
                        dmc.Text("Top-level context", size="xs", c="dimmed"),
                    ],
                    gap=2,
                ),
                dmc.Badge(id="stat-scope-badge", variant="light", color="indigo", radius="sm"),
            ],
            justify="space-between",
        )
    ],
)


home_layout = dmc.MantineProvider(
    withCssVariables=True,
    children=[ 
        dmc.Paper(
                    withBorder=False,
                    radius=0,
                    shadow="xs",
                    p="md",
                    mb=12,
                    style={
                        "backgroundColor": "#1F53C9",  
                        "color": "white",
                    },
                    children=dmc.Group(
                        justify="space-between",
                        align="center",
                        children=[
                            dmc.Stack(
                                gap=2,
                                children=[
                                    dmc.Text(
                                        "NHS Referral to Treatment Waiting Times Dashboard",
                                        fw=650, fz=25, c="white"
                                    ),
                                    dmc.Text(
                                        "Explore waiting times and pathway trends",
                                        fz="sm", c="rgba(255,255,255,0.85)"  
                                    ),
                                ],
                            ),
                            dmc.Button(
                                id="help-open-btn-home",
                                leftSection=dash_iconify.DashIconify(icon="mdi:help-circle-outline", width=18, color="white"),
                                children="Help",
                                variant="subtle", 
                                color="white",
                                size="sm",
                                styles={"color": "white"},
                            ),
                        ],
                    ),
                ),
        dmc.Container([

            dmc.Grid([
                # Left Panel (Controls)
                dbc.Col([
                    dmc.Paper([
                        dmc.SegmentedControl(
                            id="granularity-selector",
                            value="National",
                            data=["National", "Regional"],
                            fullWidth=True,
                            size="sm",
                            mb=10
                        ),
                        dmc.RadioGroup(
                            id="pathway-selector",
                            label="Select Pathway Type",
                            children=[
                                dmc.Stack([
                                    dmc.Radio(label="Incomplete", value="Incomplete"),
                                    dmc.Radio(label="Admitted", value="Admitted"),
                                    dmc.Radio(label="Non-Admitted", value="Non-Admitted"),
                                    dmc.Radio(label="New Referrals", value="New-Referrals"),
                                ])
                            ],
                            value="Incomplete",
                        ),
                        dmc.Space(h=10),
                        dmc.Select(
                            id="region-dropdown",
                            label="Select Region",
                            placeholder="Choose region",
                            data=[],
                            style={"display": "none"}  # hidden by default
                        ),
                        dmc.Space(h=20),
                        dmc.Button("Go", id="go-button", fullWidth=True),
                        html.Div(id="go-warning", style={"marginTop": "1rem"}),
                        # --- Stats grid---
                        dmc.Space(h=12),

                        nhs_header_card,

                        dmc.SimpleGrid(
                            cols=2,
                            spacing="sm",
                            verticalSpacing="md",
                            children=[
                                StatCard(
                                    title="Regions",
                                    value_id="stat-regions-value",
                                    caption="National total or selected region",
                                    icon="mdi:map-legend",
                                    color="teal",
                                ),
                                StatCard(
                                    title="ICBs",
                                    value_id="stat-icbs-value",
                                    caption="Unique Integrated Care Boards",
                                    icon="mdi:vector-polygon",
                                    color="cyan",
                                ),
                                StatCard(
                                    title="Providers",
                                    value_id="stat-providers-value",
                                    caption="NHS providers (with geocodes)",
                                    icon="mdi:hospital-building",
                                    color="blue",
                                ),
                                 StatCard(
                                    title="Estimated Population",  
                                    value_id="stat-population-value",
                                    caption="National or region population",
                                    icon="mdi:account-group",
                                    color="violet",
                                ),
                            ],
                        ),
                    ], shadow="xs", p="md", withBorder=True)
                ], width=4),

                # Right Panel (Map)
                dbc.Col([
                    dl.Map(
                        id="region-map",
                        center=[53.5, -1.5],
                        zoom=6,
                        minZoom=6,
                        maxZoom=10,
                        maxBounds=[[49.5, -6.5], [56.2, 2.5]],
                        style={"width": "100%", "height": "90vh"},
                        children=[
                            dl.TileLayer(
                                url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                                attribution='&copy; <a href="https://carto.com/">CARTO</a> contributors'
                            ),
                            dl.GeoJSON(
                                id="region-boundaries",
                                data=get_all_regions_geojson(),
                                options={"style": {"color": "#004a91", "weight": 2, "fillOpacity": 0}},
                                zoomToBoundsOnClick=True,
                            ),
                            dl.GeoJSON(
                                id="selected-region",
                                data={"type": "FeatureCollection", "features": []},
                                options={"style": {
                                    "fillColor": "#0078d4", "color": "#004a91", "weight": 3, "fillOpacity": 0.3
                                }},
                            ),
                            
                        ]
                    )
                ], width=8, style={"display": "flex", "alignItems": "stretch"})
            ], gutter="xl"),
        ], fluid=True),

        # --- Drawer that opens on click ---
        dmc.Drawer(
            id="help-drawer-home",
            title= dmc.Text("Welcome to the NHS Referral to Treatment Wait Times Dashboard", fw=700, fz="lg"),
            opened=False,
            position="right",
            size=420,
            overlayProps={"opacity": 0.15, "blur": 1.5},
            padding="md",
            zIndex=5000,
            children=html.Div(id="help-body-home"),
        ),
    ]
)
