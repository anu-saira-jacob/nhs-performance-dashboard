import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
import pandas as pd
from dash.exceptions import PreventUpdate
from unittest.mock import patch
import dash_mantine_components as dmc
from dash import no_update
import callbacks.home_callbacks as home  # module alias for patching ctx

# Import the functions under test
from callbacks.home_callbacks import (
        toggle_region_dropdown,
        populate_region_dropdown, 
        sync_region_selection, 
        go_button_handler, 
        open_help_home,
        fill_stats,
        _fmt,
    )


# -----------------------------------------------------------------------------
# toggle_region_dropdown(granularity)
# -----------------------------------------------------------------------------

def test_toggle_region_dropdown_regional():
    # Regional granularity should show the region dropdown
    style = toggle_region_dropdown("Regional")
    assert style == {"display": "block"}


def test_toggle_region_dropdown_national():
    # National (or anything else) should hide it
    style = toggle_region_dropdown("National")
    assert style == {"display": "none"}


# -----------------------------------------------------------------------------
# populate_region_dropdown(granularity)
# -----------------------------------------------------------------------------

@patch("callbacks.home_callbacks.get_all_regions")
def test_populate_region_dropdown_regional(mock_get_regions):
    # When granularity is Regional, we populate the dropdown with region records
    mock_df = pd.DataFrame([
        {"nhs_code": "R001", "name": "North East and Yorkshire"},
        {"nhs_code": "R002", "name": "North West"},
    ])
    mock_get_regions.return_value = mock_df

    data = populate_region_dropdown("Regional")

    # The component expects a list of dicts
    assert data == mock_df.to_dict("records")
    # Sanity-check a couple of entries
    assert data[0]["nhs_code"] == "R001"
    assert data[1]["name"] == "North West"


def test_populate_region_dropdown_non_regional():
    # If granularity isn't Regional, the callback should not update anything
    with pytest.raises(PreventUpdate):
        populate_region_dropdown("National")


# Case 1: dropdown selection drives the state (no clickData).
# Expect: map center/zoom, dropdown mirrors value, selected feature, and clean meta.
@patch("callbacks.home_callbacks.get_all_regions_geojson")
def test_sync_region_selection_from_dropdown(mock_geo):
    nhs_code = "R001"
    feature = {
        "type": "Feature",
        "properties": {
            "nhs_code": nhs_code,
            "name": "North East",
            "center_lat": 54.5,
            "center_lon": -1.2,
        },
        "geometry": {"type": "Polygon", "coordinates": []},
    }
    mock_geo.return_value = {"type": "FeatureCollection", "features": [feature]}

    center, zoom, dd_value, selected_fc, meta = sync_region_selection(nhs_code, None)

    # Map view should center to the feature and zoom to 8 (as defined in the callback)
    assert center == [54.5, -1.2]
    assert zoom == 8

    # Dropdown value echoes the chosen region code
    assert dd_value == nhs_code

    # Selected overlay should contain exactly one feature — the match
    assert selected_fc["type"] == "FeatureCollection"
    assert len(selected_fc["features"]) == 1
    assert selected_fc["features"][0]["properties"]["nhs_code"] == nhs_code

    # Meta contains a minimal, clean payload
    assert meta == {"nhs_code": nhs_code, "name": "North East"}


# Case 2: clickData drives the state (no dropdown value).
# Expect: same outputs as above, using the code from clickData.
@patch("callbacks.home_callbacks.get_all_regions_geojson")
def test_sync_region_selection_from_click(mock_geo):
    nhs_code = "R002"
    feature = {
        "type": "Feature",
        "properties": {
            "nhs_code": nhs_code,
            "name": "North West",
            "center_lat": 53.5,
            "center_lon": -2.1,
        },
        "geometry": {"type": "Polygon", "coordinates": []},
    }
    mock_geo.return_value = {"type": "FeatureCollection", "features": [feature]}

    click_data = {"properties": {"nhs_code": nhs_code}}

    center, zoom, dd_value, selected_fc, meta = sync_region_selection(None, click_data)

    assert center == [53.5, -2.1]
    assert zoom == 8
    assert dd_value == nhs_code
    assert selected_fc["features"][0]["properties"]["nhs_code"] == nhs_code
    assert meta == {"nhs_code": nhs_code, "name": "North West"}


# Case 3: neither dropdown nor clickData is set → do not update.
def test_sync_region_selection_no_input():
    with pytest.raises(PreventUpdate):
        sync_region_selection(None, None)


# Case 4: code provided but no matching feature in geojson → do not update.
@patch("callbacks.home_callbacks.get_all_regions_geojson")
def test_sync_region_selection_code_not_found(mock_geo):
    # GeoJSON has R999, but input requests R123 — should PreventUpdate
    mock_geo.return_value = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "nhs_code": "R999",
                    "name": "Somewhere",
                    "center_lat": 52.0,
                    "center_lon": -1.0,
                },
                "geometry": {"type": "Polygon", "coordinates": []},
            }
        ],
    }

    with pytest.raises(PreventUpdate):
        sync_region_selection("R123", None)


# Guard: wrong trigger id -> PreventUpdate
def test_go_button_handler_wrong_trigger():
    with patch.object(home, "ctx") as mock_ctx:
        mock_ctx.triggered_id = "something-else"
        with pytest.raises(PreventUpdate):
            go_button_handler(n_clicks=1, granularity="National", pathway="Incomplete", region_meta=None)


# Guard: no clicks -> PreventUpdate
def test_go_button_handler_no_clicks():
    with patch.object(home, "ctx") as mock_ctx:
        mock_ctx.triggered_id = "go-button"
        with pytest.raises(PreventUpdate):
            go_button_handler(n_clicks=0, granularity="National", pathway="Incomplete", region_meta=None)


# Guard: missing granularity or pathway -> PreventUpdate
def test_go_button_handler_missing_inputs():
    with patch.object(home, "ctx") as mock_ctx:
        mock_ctx.triggered_id = "go-button"
        # Missing granularity
        with pytest.raises(PreventUpdate):
            go_button_handler(n_clicks=1, granularity=None, pathway="Incomplete", region_meta=None)
        # Missing pathway
        with pytest.raises(PreventUpdate):
            go_button_handler(n_clicks=1, granularity="National", pathway=None, region_meta=None)


# Edge: Regional view without region -> returns red Alert and no_update for url/granularity
def test_go_button_handler_regional_without_region():
    with patch.object(home, "ctx") as mock_ctx:
        mock_ctx.triggered_id = "go-button"
        url, warning, stored_gran = go_button_handler(
            n_clicks=1,
            granularity="Regional",
            pathway="Incomplete",
            region_meta=None,
        )

        # URL and granularity are not updated
        assert url is no_update
        assert stored_gran is no_update

        # Extract props from the Mantine Alert and check its content
        props = warning.to_plotly_json().get("props", {})
        assert props.get("color") == "red"
        assert "No Region Selected" in props.get("title", "")


# Edge: National view but region selected -> returns yellow Alert and no_update
def test_go_button_handler_national_with_region_selected():
    with patch.object(home, "ctx") as mock_ctx:
        mock_ctx.triggered_id = "go-button"
        url, warning, stored_gran = go_button_handler(
            n_clicks=1,
            granularity="National",
            pathway="Incomplete",
            region_meta={"nhs_code": "R001", "name": "North East"},
        )

        assert url is no_update
        assert stored_gran is no_update

        props = warning.to_plotly_json().get("props", {})
        assert props.get("color") == "yellow"
        assert "Switch to Regional Tab" in props.get("title", "")


# Happy path: valid inputs -> routes correctly and stores granularity
def test_go_button_handler_valid_route_incomplete():
    with patch.object(home, "ctx") as mock_ctx:
        mock_ctx.triggered_id = "go-button"
        url, warning, stored_gran = go_button_handler(
            n_clicks=1,
            granularity="National",
            pathway="Incomplete",
            region_meta=None,
        )

        assert url == "/incomplete"
        assert warning is None
        assert stored_gran == "National"


# Another route mapping to show coverage (New-Referrals mapping/casing)
def test_go_button_handler_valid_route_new_referrals():
    with patch.object(home, "ctx") as mock_ctx:
        mock_ctx.triggered_id = "go-button"
        url, warning, stored_gran = go_button_handler(
            n_clicks=1,
            granularity="National",
            pathway="New-Referrals",
            region_meta=None,
        )

        assert url == "/new-referrals"
        assert warning is None
        assert stored_gran == "National"

# No clicks -> nothing changes
def test_open_help_home_no_click():
    opened, body = open_help_home(0)
    assert opened is no_update
    assert body is no_update


# Click -> drawer opens and help content is rendered
@patch.object(home, "_render_min_help")
def test_open_help_home_click(mock_render):
    # Provide fake help content for the test
    with patch.object(home, "PAGE_HELP_MIN", {"home": {"some": "content"}}):
        mock_render.return_value = "HELP_RENDERED"

        opened, body = open_help_home(1)

        assert opened is True
        assert body == "HELP_RENDERED"
        mock_render.assert_called_once_with({"some": "content"})


# Regional granularity with a valid region_meta should display the region name
# and use regional counters (ICBs, providers, population).
@patch("callbacks.home_callbacks.count_icbs_by_region")
@patch("callbacks.home_callbacks.count_providers_by_region")
@patch("callbacks.home_callbacks.get_population_by_region")
def test_fill_stats_regional(mock_pop, mock_providers, mock_icbs):
    # Arrange: control the regional stats via mocks
    mock_icbs.return_value = 15
    mock_providers.return_value = 7
    mock_pop.return_value = 1_250_000

    # Act
    badge, regions_val, icbs_val, providers_val, pop_val = fill_stats(
        "Regional", {"nhs_code": "R001", "name": "North East"}
    )

    # Assert: badge and region label
    assert badge == "Region: North East"
    assert regions_val == "North East"

    # Assert: values reflect the mocked regional stats, formatted by _fmt
    assert icbs_val == _fmt(mock_icbs.return_value)
    assert providers_val == _fmt(mock_providers.return_value)
    assert pop_val == _fmt(mock_pop.return_value)


# National granularity should call national count functions and show "National" badge
# and use national counts, ignoring any region_meta.
@patch("callbacks.home_callbacks.count_regions_national")
@patch("callbacks.home_callbacks.count_icbs_national")
@patch("callbacks.home_callbacks.count_providers_national")
@patch("callbacks.home_callbacks.get_population_national")
def test_fill_stats_national(mock_pop, mock_providers, mock_icbs, mock_regions):
    
    # Setup mock return values
    mock_regions.return_value = 7
    mock_icbs.return_value = 42
    mock_providers.return_value = 120
    mock_pop.return_value = 5_500_000

    # Call with National granularity and no region_meta
    badge, regions_val, icbs_val, providers_val, pop_val = fill_stats("National", None)

    # Assert against expected formatted values
    assert badge == "National"
    assert regions_val == _fmt(mock_regions.return_value)
    assert icbs_val == _fmt(mock_icbs.return_value)
    assert providers_val == _fmt(mock_providers.return_value)
    assert pop_val == _fmt(mock_pop.return_value)


# Edge case: Regional granularity but region_meta missing nhs_code -> fallback to National
@patch("callbacks.home_callbacks.count_regions_national")
@patch("callbacks.home_callbacks.count_icbs_national")
@patch("callbacks.home_callbacks.count_providers_national")
@patch("callbacks.home_callbacks.get_population_national")
def test_fill_stats_regional_missing_code(mock_pop, mock_providers, mock_icbs, mock_regions):
    
    # Setup mock return values
    mock_regions.return_value = 7
    mock_icbs.return_value = 42
    mock_providers.return_value = 120
    mock_pop.return_value = 5_500_000

    # Call with Regional granularity but incomplete region_meta
    badge, regions_val, icbs_val, providers_val, pop_val = fill_stats("Regional", {"name": "X"})

    # Assert (falls back to national branch)
    assert badge == "National"
    assert regions_val == _fmt(mock_regions.return_value)
    assert icbs_val == _fmt(mock_icbs.return_value)
    assert providers_val == _fmt(mock_providers.return_value)
    assert pop_val == _fmt(mock_pop.return_value)

