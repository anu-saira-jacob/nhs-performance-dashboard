import dash_mantine_components as dmc

from dash import (
    callback,
    Output,
    Input,
    State,
    no_update,
    ctx,
)
from dash.exceptions import PreventUpdate

from queries import (
    get_all_regions_geojson,
    get_all_regions,
    count_regions_national,
    count_icbs_national,
    count_icbs_by_region,
    count_providers_national,
    count_providers_by_region,
    get_population_by_region,
    get_population_national,
)

from utils.constants import _render_min_help
from utils.help_text import PAGE_HELP_MIN



# ------This callback will:
# Listen to granularity-selector
#If "Regional" → show region-dropdown
# Else → hide it
@callback(
    Output("region-dropdown", "style"),
    Input("granularity-selector", "value")
)
def toggle_region_dropdown(granularity):
    if granularity == "Regional":
        return {"display": "block"}
    return {"display": "none"}


# This callback will: 
#  # Listen to granularity-selector
# If "Regional" → populate region-dropdown with regions
@callback(
    Output("region-dropdown", "data"),
    Input("granularity-selector", "value")
)
def populate_region_dropdown(granularity):
    if granularity != "Regional":
        raise PreventUpdate

    df = get_all_regions()  
    return df.to_dict("records")


# This callback will:
# Listen to region-dropdown and region-boundaries clickData
# If region-dropdown value or clickData is set, update map center and zoom
# If clickData is set, update selected-region data
# If dropdown value is set, update selected-region data
@callback(
    Output("region-map", "center"),
    Output("region-map", "zoom"),
    Output("region-dropdown", "value"),
    Output("selected-region", "data"),  # highlight on map
    Output("selected-region-meta", "data", allow_duplicate=True),  # store clean region data
    Input("region-dropdown", "value"),
    Input("region-boundaries", "clickData"),
    prevent_initial_call=True
)
def sync_region_selection(dropdown_value, click_data):
    geojson = get_all_regions_geojson()

    nhs_code = None
    if click_data and click_data.get("properties", {}).get("nhs_code"):
        nhs_code = click_data["properties"]["nhs_code"]
    elif dropdown_value:
        nhs_code = dropdown_value
    else:
        raise PreventUpdate

    for feature in geojson["features"]:
        if feature["properties"]["nhs_code"] == nhs_code:
            center = [
                feature["properties"]["center_lat"],
                feature["properties"]["center_lon"]
            ]
            name = feature["properties"]["name"]
            selected_geojson = {
                "type": "FeatureCollection",
                "features": [feature]
            }

            return center, 8, nhs_code, selected_geojson, {
                "nhs_code": nhs_code,
                "name": name
            }

    raise PreventUpdate


# This callback will:
# Listen to go-button click
# If granularity or pathway is not set, raise PreventUpdate
# If regional view but no region selected, show warning
# If national view but region was selected, show warning
# If all good, route to appropriate page and store granularity and region meta
@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("go-warning", "children"),
    Output("selected-granularity", "data", allow_duplicate=True),  # ONLY store granularity here
    Input("go-button", "n_clicks"),
    State("granularity-selector", "value"),
    State("pathway-selector", "value"),
    State("selected-region-meta", "data"),
    prevent_initial_call=True
)
def go_button_handler(n_clicks, granularity, pathway, region_meta):

    if ctx.triggered_id != "go-button":
        raise PreventUpdate


    if not n_clicks or n_clicks == 0:
        raise PreventUpdate


    if not granularity or not pathway:
        raise PreventUpdate


    # Edge Case: Regional view but no region selected
    if granularity == "Regional" and not region_meta:
        return no_update, dmc.Alert(
            title="No Region Selected",
            color="red",
            children="Please select a region before proceeding to the regional dashboard.",
            withCloseButton=True
        ), no_update

    # Edge Case: National view but region was selected (e.g. from map click)
    if granularity == "National" and region_meta:
        return no_update, dmc.Alert(
            title="Switch to Regional Tab",
            color="yellow",
            children="You’ve selected a region, but are still in the National view. Please switch to 'Regional' tab to view regional data.",
            withCloseButton=True
        ), no_update

    # All good → proceed to route
    route_map = {
        "Incomplete": "/incomplete",
        "Admitted": "/admitted",
        "Non-Admitted": "/non-admitted",
        "New-Referrals": "/new-referrals"  # match casing with layout routing
    }

    return route_map.get(pathway, "/"), None, granularity


@callback(
    Output("help-drawer-home", "opened"),
    Output("help-body-home", "children"),
    Input("help-open-btn-home", "n_clicks"),
    prevent_initial_call=True,
)
def open_help_home(n_clicks):
    if not n_clicks:
        return no_update, no_update
    content = PAGE_HELP_MIN["home"]
    body = _render_min_help(content)
    return True, body


def _fmt(value):
    """Format stats values with K, M suffix for readability."""
    if value is None:
        return "–"
    try:
        value = int(value)
    except Exception:
        return str(value)

    if value >= 1_000_000:
        return f"{value/1_000_000:.1f}M".rstrip("0").rstrip(".")
    elif value >= 1_000:
        return f"{value/1_000:.1f}K".rstrip("0").rstrip(".")
    return str(value)

@callback(
    Output("stat-scope-badge", "children"),
    Output("stat-regions-value", "children"),
    Output("stat-icbs-value", "children"),
    Output("stat-providers-value", "children"),
    Output("stat-population-value", "children"),   
    Input("granularity-selector", "value"),
    Input("selected-region-meta", "data"),
    prevent_initial_call=False,
)
def fill_stats(granularity, region_meta):
    if granularity == "Regional" and region_meta and region_meta.get("nhs_code"):
        region_code = region_meta["nhs_code"]
        region_name = region_meta.get("name", "")
        icbs = count_icbs_by_region(region_code)
        providers = count_providers_by_region(region_code)
        population = get_population_by_region(region_code)

        # Regions card shows the region NAME 
        return (
            f"Region: {region_name}",
            region_name,
            _fmt(icbs),
            _fmt(providers),
            _fmt(population),
        )

    # National view
    regions = count_regions_national()   
    icbs = count_icbs_national()        
    providers = count_providers_national()
    population = get_population_national()

    return (
        "National",
        _fmt(regions),
        _fmt(icbs),
        _fmt(providers),
        _fmt(population),
    )
