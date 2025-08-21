import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import dash_leaflet as dl
import dash_mantine_components as dmc
import dash_iconify

from dash import (
    callback,
    Output,
    Input,
    State,
    no_update,
    html,
    callback_context as ctx,
)
from dash.exceptions import PreventUpdate
from dash_extensions.javascript import assign

from queries import (
    get_monthly_treatment_comparison,
    get_top_or_bottom_treatments,
    get_all_treatment_functions,
    get_incomplete_trend,
    get_icb_rtt_for_region_incomplete,
    get_icb_boundaries_geojson,
    get_region_bounds,
    get_ccg_imd_geojson,
    get_icb_imd_scatter_data_incomplete,
    get_national_metric_value_incomplete,
)

from utils.constants import (
    METRIC_MODE_LABELS,
    build_trend_figure,
    _wrap_label,
    _render_min_help,
    _metric_formatting,
)
from utils.help_text import (
    METRIC_HELP_TEXT,
    INCOMPLETE_DROPDOWN_MAP,
    build_help_icon,
    PAGE_HELP_MIN,
)


@callback(
    Output("incomplete-line-chart", "figure"),
    Input("dummy-trigger", "children"),
    Input("metric-selector", "value"),
    State("selected-granularity", "data"),
    State("selected-region-meta", "data"),
)
def plot_median_wait(_, selected_metric, granularity, selected_region_meta):

    if not selected_metric:
        raise PreventUpdate

    # Determine geo_level and code
    geo_level = "National"
    nhs_code = None
    region_name = None

    if granularity == "Regional":
        if not selected_region_meta["nhs_code"]:
            return go.Figure().update_layout(title="Please select a region", height=400)
        geo_level = "Region"
        nhs_code = selected_region_meta["nhs_code"]
        region_name = selected_region_meta["name"]

    # Fetch data
    df = get_incomplete_trend(selected_metric, geo_level=geo_level, nhs_code=nhs_code)
    if df.empty:
        return go.Figure().update_layout(title="No data found", height=400)

    # Title 
    prefix = "National Trend" if geo_level == "National" else f"Regional Trend – {region_name}"
    title = f"{prefix} – {selected_metric}"

    # build figure via helper to maintain formatting 
    fig = build_trend_figure(
        df=df,
        metric=selected_metric,
        title=title,
        line_color="#2a9d8f",   
        font_family="Segoe UI",
        show_rolling=True,        
    )

    return fig




# ------CALLBACKS FOR TREATMENT FUNCTION DROPDOWN-------
@callback(
    Output("treatment-function-checklist", "data"), 
    Input("dummy-trigger", "children"),
    State("selected-granularity", "data"),
    State("selected-region-meta", "data"),
)
def populate_treatment_dropdown(_, selected_granularity, selected_region_meta):

    geo_level = "National"
    nhs_code = None
    
    if selected_granularity == "Regional":
        geo_level = "Region"
        nhs_code = selected_region_meta["nhs_code"]

    df = get_all_treatment_functions(geo_level=geo_level, nhs_code=nhs_code)

    options = [
        {"label": row["treatment_function"], "value": row["treatment_function_code"]}
        for _, row in df.iterrows()
    ]
    return options




@callback(
    Output("bar-chart-comparison", "figure"),
    Output("selection-warning", "children"),
    Input("display-chart-btn", "n_clicks"),
    Input("dummy-trigger", "children"),
    Input("metric-selector", "value"),
    State("month-selector", "value"),
    State("chart-mode", "value"),
    State("treatment-function-checklist", "value"),
    State("selected-granularity", "data"),
    State("selected-region-meta", "data"),
    prevent_initial_call=False,
)
def update_bar_chart(n_clicks, dummy_trigger, selected_metric ,date_val, mode, selected_codes, selected_granularity, selected_region_meta):

    colors = ["#4E79A7", "#F28E2B", "#E15759", "#76B7B2", "#59A14F"]

    fig = go.Figure()

    geo_level = "National"
    nhs_code = None
    region_name = None

    if selected_granularity == "Regional":
        geo_level = "Region"
        nhs_code = selected_region_meta["nhs_code"]
        region_name = selected_region_meta["name"]

    # Determine date
    if isinstance(date_val, datetime.date):
        dt = date_val
    elif isinstance(date_val, str):
        dt = datetime.datetime.fromisoformat(date_val)
    else:
        dt = datetime.date(2023, 4, 1)  #  default on first load

    year, month = dt.year, dt.month

    # Determine mode
    if not mode:
        mode = "top"  #  default to 'Top 5 longest waits'

    # Branch based on mode
    if mode == "manual":
        if (not selected_codes or len(selected_codes) < 3) and n_clicks:
            return (
                fig,
                "Please select at least 3 treatment functions to display the chart.",
            )

        selected_codes = selected_codes[:5]
        df = get_monthly_treatment_comparison(year, month, selected_codes, geo_level, nhs_code, selected_metric)
    else:
        order = "desc" if mode == "top" else "asc"
        df = get_top_or_bottom_treatments(year, month, order, geo_level, nhs_code, 5, selected_metric)

    if df.empty:
        fig.update_layout(title="No data available", height=400)
        return fig, ""

    
    if geo_level == "Region":
        title = f"{selected_metric} By Treatment Function – {region_name} ({dt.strftime('%B %Y')})"
    else:
        title = f"{selected_metric} By Treatment Function – National ({dt.strftime('%B %Y')})"


    total_val = None

    # Format y-axis and hover text based on metric
    # Convert to percentage if required
    if "%" in selected_metric:
        df["value"] *= 100
        yaxis_title = "Percentage (%)"
        hover_fmt = "%{y:.1f}%"
    elif "waiting time" in selected_metric.lower():
        yaxis_title = "Waiting time (weeks)"
        hover_fmt = "%{y:.2f} weeks"
    elif "total" in selected_metric.lower():
        yaxis_title = "Total Count"
        hover_fmt = "%{y:,.0f}"
    else:
        yaxis_title = "Value"
        hover_fmt = "%{y:.2f}"


    
    for i, row in enumerate(df.itertuples()):
        fig.add_trace(
            go.Bar(
                x=[i],
                y=[row.value],
                name=row.treatment_function,
                marker=dict(color=colors[i % len(colors)]),  # assign color
                hovertemplate = f"<b>{row.treatment_function}</b><br>{hover_fmt}<extra></extra>"
            )
        )



    fig.update_layout(
        height=450,
        bargap=0.2,
        title=title,
        yaxis=dict(
            title=yaxis_title,
            range=[0, max(df["value"].max(), total_val or 0) * 1.2],  
            gridcolor="#DDE2E6",
        ),
        xaxis=dict(
            title="Treatment Type",
            tickvals=[],  
            showticklabels=False,
        ),
        font=dict(family="Segoe UI", size=14),
        margin={"t": 40, "b": 60},
        showlegend=True,
    )

    return fig, ""

# MANUAL SELECTION SECTION FOR INCOMPLETE PATHWAY-----
@callback(
    Output("manual-selection-section", "style"),
    Input("chart-mode", "value"),
)
def toggle_manual_section(mode):
    if mode == "manual":
        return {"display": "block"}
    else:
        return {"display": "none"}
    

@callback(
    Output("chart-mode", "options"),
    Output("chart-mode", "value"),
    Input("metric-selector", "value"),
    prevent_initial_call=False  
)
def update_chart_mode_options(selected_metric):
    if not selected_metric:
        raise PreventUpdate
    options = METRIC_MODE_LABELS.get(selected_metric, ["default"])
    # Always reset to a valid default when metric changes
    return options, "top"

@callback(
    Output("incomplete-imd-block", "style"),
    Input("selected-granularity", "data"),
    Input("url", "pathname"),   
    prevent_initial_call=False
)
def toggle_imd_block(granularity, pathname):
    if pathname == "/incomplete" and granularity == "Regional":
        return {"display": "block"}
    return {"display": "none"}

@callback(
    Output("incomplete-icb-rtt-bars", "figure"),
    Input("dummy-trigger", "children"),
    Input("metric-selector", "value"),
    Input("month-selector", "value"),
    Input("incomplete-selected-icb", "data"), 
    State("selected-region-meta", "data"),
    State("selected-granularity", "data"),
)
def render_icb_rtt_bars(_, metric, month_value, selected_icb, region_meta, granularity):
    if granularity != "Regional" or not region_meta or not month_value:
        return px.bar(pd.DataFrame(columns=["org_name", "value"]), x="value", y="org_name", orientation="h")

    month_dt = datetime.date.fromisoformat(month_value) if isinstance(month_value, str) else month_value
    year, month = month_dt.year, month_dt.month

    region_code = region_meta.get("nhs_code")
    df = get_icb_rtt_for_region_incomplete(year, month, metric, region_code)
    if df is None or df.empty:
        return px.bar(pd.DataFrame(columns=["org_name", "value"]), x="value", y="org_name", orientation="h")

    # Short display labels
    df_plot = df.copy()
    df_plot["short_name"] = (
        df_plot["org_name"]
        .str.replace(r"^NHS\s+", "", regex=True)
        .str.replace(r"\s+INTEGRATED CARE BOARD$", "", regex=True)
        .str.replace(" and ", " & ", regex=False)
    )
    df_plot["short_name_wrapped"] = df_plot["short_name"].apply(_wrap_label)

    # Scale percentage metric before plotting so x and hover show correct values
    if "%" in (metric or ""):
        df_plot["value"] = df_plot["value"] * 100.0

    # Colors: highlight selected ICB
    highlight, base = "#1f50b9", "#548ad6"
    colors = [highlight if (selected_icb and oc == selected_icb) else base for oc in df_plot["org_code"]]

    # Build horizontal bars (use wrapped labels on y)
    fig = px.bar(df_plot, x="value", y="short_name_wrapped", orientation="h", text=None)

    # Customdata: code (for selection), short (for internal), full name (for hover)
    fig.update_traces(
        marker_color=colors,
        customdata=df_plot[["org_code", "short_name", "org_name"]].to_numpy(),
    )

    # Metric-aware hover line 
    m = (metric or "").lower()
    if "%" in (metric or ""):
        hover_line = f"{metric}: %{{x:.1f}}%"
    elif "waiting time" in m:
        hover_line = f"{metric}: %{{x:.2f}} weeks"
    elif "total" in m or "count" in m or "number" in m:
        hover_line = f"{metric}: %{{x:,.0f}}"
    else:
        hover_line = f"{metric}: %{{x:.2f}}"

    fig.update_traces(
        hovertemplate="<b>%{customdata[2]}</b><br>" + hover_line + "<extra></extra>"
    )

    fig.update_layout(
        margin=dict(l=160, r=8, t=10, b=40),
        yaxis=dict(title=None, automargin=False, tickfont=dict(size=12)),
        xaxis=dict(title=metric, automargin=False),
        showlegend=False,
    )
    return fig

# small helper: recolor existing figure in-place
def _recolor_bars(fig, selected_code):
    if not fig or not fig.get("data"):
        return fig
    trace = fig["data"][0]
    cd = trace.get("customdata")
    if cd is None:
        return fig
    base = "#548ad6"
    hi = "#1f50b9"
    colors = [hi if (selected_code and row[0] == selected_code) else base for row in cd]
    if "marker" not in trace:
        trace["marker"] = {}
    trace["marker"]["color"] = colors
    return fig

# small helper: center from bounds and a reasonable zoom
def _center_from_bounds(bounds):
    (s, w), (n, e) = bounds
    return [(s + n) / 2.0, (w + e) / 2.0]

def _zoom_from_bounds(bounds):
    (s, w), (n, e) = bounds
    lat_span = max(1e-6, abs(n - s))
    lon_span = max(1e-6, abs(e - w))
    span = max(lat_span, lon_span)
    if span < 0.35:
        z = 10
    elif span < 0.6:
        z = 9
    elif span < 1.2:
        z = 8
    else:
        z = 7
    return z

@callback(
    Output("incomplete-selected-icb", "data"),
    Output("incomplete-imd-map-map", "center"),
    Output("incomplete-imd-map-map", "zoom"),
    Output("incomplete-icb-selected", "data"),
    Output("incomplete-icb-rtt-bars", "figure", allow_duplicate=True),
    Input("incomplete-icb-rtt-bars", "clickData"),           # bar click
    Input("incomplete-icb-layer", "clickData"),              # map click
    Input("incomplete-clear-icb-selection", "n_clicks"),     # clear
    State("incomplete-icb-rtt-bars", "figure"),              # current figure to recolor
    State("metric-selector", "value"),
    State("month-selector", "value"),
    State("selected-granularity", "data"),
    State("selected-region-meta", "data"),
    prevent_initial_call=True,
)
def select_icb(bar_click, map_click, clear_clicks, current_fig, metric, month_value, granularity, region_meta):
    # Guard
    if granularity != "Regional" or not region_meta:
        raise PreventUpdate
    region_code = region_meta.get("nhs_code")
    if not region_code:
        raise PreventUpdate

    triggered = ctx.triggered_id

    # Ignore the ICB layer's initial mount noise
    if triggered == "incomplete-icb-layer" and (not map_click or not map_click.get("properties")):
        raise PreventUpdate

    # 1) Clear button → reset selection, clear map highlight, zoom out to region, recolor bars to base
    if triggered == "incomplete-clear-icb-selection" and clear_clicks:
        # Reset map view to region
        region_bounds = get_region_bounds(region_code)
        center = _center_from_bounds(region_bounds) if region_bounds else no_update
        zoom = _zoom_from_bounds(region_bounds) if region_bounds else no_update

        # Clear selected layer
        empty_fc = {"type": "FeatureCollection", "features": []}

        # Recolor existing bars to base (no selection)
        fig = _recolor_bars(current_fig, selected_code=None)

        return None, center, zoom, empty_fc, fig

    # 2) Bar click → get icb_code from bar clickData
    icb_code = None
    if triggered == "incomplete-icb-rtt-bars" and bar_click:
        pts = bar_click.get("points") or []
        if pts and pts[0].get("customdata"):
            icb_code = pts[0]["customdata"][0]  # [org_code, short_name]

    # 3) Map click → get icb_code from feature props
    elif triggered == "incomplete-icb-layer" and map_click:
        props = map_click.get("properties") or map_click.get("feature", {}).get("properties", {})
        icb_code = props.get("icb_code")

    if not icb_code:
        raise PreventUpdate

    # Locate the clicked feature for center/bounds and selected outline
    icb_fc = get_icb_boundaries_geojson(region_code)
    feats = icb_fc.get("features", [])
    match = next((f for f in feats if f["properties"].get("icb_code") == icb_code), None)
    if not match:
        raise PreventUpdate

    # bounds = match["properties"].get("bounds")
    center = match["properties"].get("center")
    selected_fc = {"type": "FeatureCollection", "features": [match]}

   
    # Recolor existing bar figure to highlight the selected ICB
    fig = _recolor_bars(current_fig, selected_code=icb_code)

    return icb_code, center, no_update, selected_fc, fig


@callback(
    Output("incomplete-imd-map", "children"),
    Input("dummy-trigger", "children"),  
    State("selected-granularity", "data"),
    State("selected-region-meta", "data"),
    prevent_initial_call=False,
)
def render_incomplete_imd_map(_, granularity, region_meta):
    
    # Only render in Regional mode with a selected region
    if granularity != "Regional" or not region_meta or not region_meta.get("nhs_code"):
        return html.Div(
            "Switch to Regional and select a region to see the IMD map.",
            style={
                "display": "flex",
                "height": "100%",
                "alignItems": "center",
                "justifyContent": "center",
                "color": "#666",
            },
        )

    region_code = region_meta["nhs_code"]

    # Data
    ccg_fc = get_ccg_imd_geojson(region_code)         
    icb_fc = get_icb_boundaries_geojson(region_code)  
    bounds = get_region_bounds(region_code)          

    # CCG choropleth style (no hover, no tooltip, non-interactive)
    ccg_style = assign("""
        function(feature, context){
            const q = feature.properties.imd_quintile;
            const colors = {1:'#7f0000', 2:'#b30000', 3:'#e34a33', 4:'#fc8d59', 5:'#fdcc8a'};
            return {
                color: '#666',
                weight: 0.5,
                fillOpacity: 0.75,
                fillColor: colors[q] || '#cccccc'
            };
        }
    """)

    # ICB outline style (make the whole polygon interactive via transparent fill)
    icb_style = assign("""
        function(feature, context){
            return {
                color: '#3f3d3d',
                weight: 1.5,
                opacity: 0.95,
                fill: true,        // <— enable fill to capture mouse events over the area
                fillOpacity: 0.0,  // <— fully transparent; still hit-testable
            };
        }
    """)

    icb_on_each = assign("""
        function(feature, layer, context){
            const label = feature.properties.icb_label || feature.properties.icb_name || '';
            layer.bindTooltip(label, {sticky: true, direction: 'top'});
        }
    """)

    # Subtle hover emphasis (slightly thicker + darker)
    icb_hover = assign("""
        function(feature, context){
            return {
                color: '#1f2937',   // darker charcoal
                weight: 2.5
            };
        }
    """)

    # style for the selected ICB (subtle but visible)
    icb_selected_style = assign("""
        function(feature, context){
            return {
                color: '#193758',   // darker charcoal
                weight: 3,
                opacity: 1,
                fill: true,
                fillOpacity: 0.0
            };
        }
    """)

    # Legend (match the CCG palette above)
    palette = {1: "#7f0000", 2: "#b30000", 3: "#e34a33", 4: "#fc8d59", 5: "#fdcc8a"}
    
    
    # Legend overlay without dl.Control
    legend_overlay = html.Div(
        [
            html.Div("IMD (CCG)", style={"fontWeight": 600, "marginBottom": "6px"}),
        ] + [
            html.Div(
                [
                    html.Span(
                        style={
                            "display": "inline-block",
                            "width": "12px",
                            "height": "12px",
                            "marginRight": "6px",
                            "backgroundColor": palette[i],
                            "border": "1px solid rgba(0,0,0,0.2)",
                        }
                    ),
                    html.Span(f"IMD quantile {i}" + (" (most deprived)" if i == 1 else " (least)" if i == 5 else "")),
                ],
                style={"display": "flex", "alignItems": "center", "marginBottom": "4px"},
            )
            for i in [1, 2, 3, 4, 5]
        ],
        style={
            "position": "absolute",
            "bottom": "10px",
            "right": "10px",
            "padding": "6px 8px",
            "background": "white",
            "border": "1px solid #ccc",
            "borderRadius": "4px",
            "boxShadow": "0 1px 2px rgba(0,0,0,0.1)",
            "fontSize": "12px",
            "zIndex": "1000",
        },
    )

    # Assemble map
    the_map = html.Div(
        [
            dl.Map(
                id="incomplete-imd-map-map",
                bounds=bounds,
                minZoom=7,
                maxZoom=10,
                maxBounds=[[49.5, -6.5], [56.2, 2.5]],   
                style={"width": "100%", "height": "520px", "borderRadius": "8px"},
                zoomControl=True,
                children=[
                    dl.TileLayer(
                        url="https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png",
                        attribution='&copy; <a href="https://carto.com/">CARTO</a> contributors'
                    ),
                    dl.GeoJSON(
                        id="incomplete-ccg-layer",
                        data=ccg_fc,
                        options=dict(style=ccg_style, interactive=False),
                    ),
                    # In your map children, keep ICB layer above CCGs and interactive
                    dl.GeoJSON(
                        id="incomplete-icb-layer",
                        data=icb_fc,
                        options=dict(style=icb_style, onEachFeature=icb_on_each, interactive=True),
                        hoverStyle=icb_hover,  # apply hover style
                    ),
                    dl.GeoJSON(
                        id="incomplete-icb-selected",
                        data={"type": "FeatureCollection", "features": []},
                        options=dict(style=icb_selected_style, interactive=False),
                    ),
                ],
            ),
            legend_overlay,  # overlay on top of the map
        ],
        style={"position": "relative"},
    )

    return the_map

@callback(
    Output("incomplete-national-imd-block", "style"),
    Input("selected-granularity", "data"),
    Input("url", "pathname"),
    prevent_initial_call=False
)
def toggle_national_imd_block(granularity, pathname):
    if pathname == "/incomplete" and granularity == "National":
        return {"display": "block"}
    return {"display": "none"}

@callback(
    Output("incomplete-national-imd-scatter", "figure"),
    Input("metric-selector", "value"),
    Input("month-selector", "value"),
    Input("selected-granularity", "data"),
    prevent_initial_call=False
)
def render_national_imd_scatter(metric, month_value, granularity):
    if granularity != "National" or not month_value:
        return px.scatter(pd.DataFrame(columns=["x", "y"]))

    month_dt = datetime.date.fromisoformat(month_value) if isinstance(month_value, str) else month_value
    year, month = month_dt.year, month_dt.month

    df = get_icb_imd_scatter_data_incomplete(year, month, metric)
    if df.empty:
        return px.scatter(pd.DataFrame(columns=["x", "y"]))

    # Reverse IMD quintile: 1 (least) → 5 (most) → Display: 1 (most) → 5 (least)
    df["imd_quintile_display"] = 6 - df["imd_quintile"].astype(int)

    # Assign bubble size (larger = more deprived, i.e. display quantile 1)
    size_map = {1: 38, 2: 30, 3: 22, 4: 16, 5: 10}
    df["bubble_size"] = df["imd_quintile_display"].map(size_map)

    # Scale RTT value if it's a percentage metric
    if "%" in metric:
        df["rtt_value"] = df["rtt_value"] * 100

    # Set up plot
    fig = px.scatter(
        df,
        x="icb_pop_2019",
        y="rtt_value",
        color="region_name",
        size="bubble_size",
        size_max=36,
        custom_data=[
            "region_name", "icb_pop_2019", "rtt_value",
            "imd_quintile_display", "icb_name"
        ],
    )

    y_title, y_format, scale_100 = _metric_formatting(metric)

    # Format the hover label line using y_format
    y_hover = f"{y_title}: {y_format.replace('%{{y', '%{{customdata[2]')}"



    # Apply custom hovertemplate
    for trace in fig.data:
        trace.hovertemplate = (
            "<b>%{customdata[4]}</b><br>"
            "Region: %{customdata[0]}<br>"
            "IMD quintile: %{customdata[3]}<br>"
            "Population: %{customdata[1]:,}<br>"
            f"{y_hover}<extra></extra>"
        )

    # Add national average line
    nat_df = get_national_metric_value_incomplete(year, month, metric)
     # Scale RTT value if it's a percentage metric
    if "%" in metric:
        nat_df.loc[0,"value"]= nat_df.loc[0,"value"] * 100
    
    if not nat_df.empty and pd.notnull(nat_df.iloc[0]["value"]):
        nat_val = float(nat_df.iloc[0]["value"])
        x_min = float(df["icb_pop_2019"].min())
        x_max = float(df["icb_pop_2019"].max())
        fig.add_trace(
            go.Scatter(
                x=[x_min, x_max],
                y=[nat_val, nat_val],
                mode="lines",
                name="National average",
                hovertemplate="National average: %{y}<extra></extra>",
                line=dict(width=2, dash="dash"),
                showlegend=True,
            )
        )

    # Layout and legend
    fig.update_layout(
        xaxis_title="Population",
        yaxis_title=y_title,
        xaxis_type="log",
        margin=dict(l=20, r=180, t=40, b=20),
        legend=dict(
            title="Region",
            x=1.02, y=1.0,
            xanchor="left", yanchor="top",
            orientation="v"
        ),
    )

    # Add IMD quintile explanation
    fig.add_annotation(
        xref="paper", yref="paper",
        x=1.0, y=0.38,
        xanchor="left", yanchor="top",
        showarrow=False,
        align="left",
        font=dict(size=12),
        text=(
            "<b>Bubble size</b><br>"
            "Quintile 1 = most deprived = largest<br>"
            "Quintile 5 = least deprived = smallest"
        ),
    )

    return fig


@callback(
    Output("help-drawer-incomplete", "opened"),
    Output("help-body-incomplete", "children"),
    Input("help-open-btn-incomplete", "n_clicks"),
    State("selected-granularity", "data"),
    prevent_initial_call=True,
)
def open_help_incomplete(n_clicks, selected_granularity):
    if not n_clicks:
        return no_update, no_update
    
    if selected_granularity == "National":
        content = PAGE_HELP_MIN["incomplete_national"]
        body = _render_min_help(content)    
    else:
        content = PAGE_HELP_MIN["incomplete_regional"]
        body = _render_min_help(content)
    return True, body




@callback(
    Output("metric-help-icon-incomplete", "children"),
    Input("metric-selector", "value")
)
def update_metric_help(selected_metric):
    if not selected_metric:
        return no_update
    key = INCOMPLETE_DROPDOWN_MAP.get(selected_metric)
    if not key:
        return no_update
    text = METRIC_HELP_TEXT["incomplete"].get(key, "")
    return build_help_icon(text)


# --- Regional subtitle ---
@callback(
    Output("incomplete-imd-regional-subtitle", "children"),
    Input("metric-selector", "value"),
    Input("month-selector", "value"),
    State("selected-granularity", "data"),
    State("selected-region-meta", "data"),
)
def update_regional_subtitle(metric, month_value, granularity, region):
    if granularity != "Regional" or not month_value:
        return ""

    month_dt = datetime.date.fromisoformat(month_value) if isinstance(month_value, str) else month_value
    month_label = month_dt.strftime("%B %Y")
    region_name = region["name"]

    return f"Showing {metric} for {month_label} in {region_name}, by ICB (map and bar chart)"



# --- National subtitle ---
@callback(
    Output("incomplete-imd-national-subtitle", "children"),
    Input("metric-selector", "value"),
    Input("month-selector", "value"),
    Input("selected-granularity", "data"),
)
def update_national_subtitle(metric, month_value, granularity):
    if granularity != "National" or not month_value:
        return ""

    month_dt = datetime.date.fromisoformat(month_value) if isinstance(month_value, str) else month_value
    month_label = month_dt.strftime("%B %Y")

    return f"Comparing ICBs by {metric} for {month_label}, in context of deprivation and population"


# --- National Title ---
@callback(
    Output("incomplete-title", "children"),
    Input("selected-granularity", "data"),
    Input("selected-region-meta", "data"),
)
def update_incomplete_title(granularity, region):
    if granularity == "National":
        title = "Incomplete RTT Pathways - National Overview (April 2022- March 2025)"
    else:
        region_name = region["name"]
        title = f"Incomplete RTT Pathways - Regional Overview: {region_name} (April 2022- March 2025)"

    return title

