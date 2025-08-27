import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from dash import html
import pytest
import pandas as pd
import plotly.graph_objects as go
from dash.exceptions import PreventUpdate
from dash import no_update
from unittest.mock import patch
import dash_leaflet as dl
import callbacks.incomplete_callbacks as icb

# Import the callback function directly
from callbacks.incomplete_callbacks import (
    plot_median_wait,
    populate_treatment_dropdown,
    update_bar_chart,
    toggle_manual_section,
    update_chart_mode_options,
    toggle_imd_block,
    render_icb_rtt_bars,
    select_icb,
    render_incomplete_imd_map,
    toggle_national_imd_block,
    render_national_imd_scatter,
    open_help_incomplete,
    update_metric_help,
    update_regional_subtitle,
    update_national_subtitle,
    update_incomplete_title,
)
from dash.exceptions import PreventUpdate
from utils.constants import METRIC_MODE_LABELS


# Positive test: plot builds with valid metric and region data
@patch("callbacks.incomplete_callbacks.get_incomplete_trend")
@patch("callbacks.incomplete_callbacks.build_trend_figure")
def test_plot_median_wait_valid(mock_build_figure, mock_get_trend):
    # Simulate non-empty DataFrame from the DB
    mock_df = pd.DataFrame({
        "year": [2024, 2024],
        "month": [1, 2],
        "value": [10.5, 12.3]
    })
    mock_get_trend.return_value = mock_df

    # Simulate the plot builder returning a dummy figure
    mock_fig = go.Figure().update_layout(title="Mocked Trend")
    mock_build_figure.return_value = mock_fig

    # Input params
    selected_metric = "Average (median) waiting time (in weeks)"
    granularity = "Regional"
    selected_region_meta = {"nhs_code": "Q45", "name": "Test Region"}

    result = plot_median_wait(1, selected_metric, granularity, selected_region_meta)

    # The returned object should be the mocked figure
    assert isinstance(result, go.Figure)
    assert result.layout.title.text == "Mocked Trend"


# Negative test: no metric selected → should raise PreventUpdate
def test_plot_median_wait_no_metric():
    with pytest.raises(PreventUpdate):
        plot_median_wait(1, None, "National", {})


@patch("callbacks.incomplete_callbacks.get_all_treatment_functions")
def test_populate_treatment_dropdown_national(mock_get_funcs):
    # Mocked DB response (National level)
    mock_df = pd.DataFrame([
        {"treatment_function_code": "A01", "treatment_function": "Test Function A"},
        {"treatment_function_code": "B02", "treatment_function": "Test Function B"},
    ])
    mock_get_funcs.return_value = mock_df

    result = populate_treatment_dropdown(
        None,  # dummy-trigger value, not used
        "National",
        {"nhs_code": None, "name": None}
    )

    assert result == [
        {"label": "Test Function A", "value": "A01"},
        {"label": "Test Function B", "value": "B02"},
    ]


@patch("callbacks.incomplete_callbacks.get_all_treatment_functions")
def test_populate_treatment_dropdown_regional(mock_get_funcs):
    # Mocked DB response (Regional level)
    mock_df = pd.DataFrame([
        {"treatment_function_code": "C03", "treatment_function": "Regional Function C"}
    ])
    mock_get_funcs.return_value = mock_df

    result = populate_treatment_dropdown(
        None,  # dummy-trigger
        "Regional",
        {"nhs_code": "R123", "name": "Some Region"}
    )

    assert result == [
        {"label": "Regional Function C", "value": "C03"}
    ]


@patch("callbacks.incomplete_callbacks.get_all_treatment_functions")
def test_populate_treatment_dropdown_empty(mock_get_funcs):
    # Empty DataFrame
    mock_df = pd.DataFrame(columns=["treatment_function_code", "treatment_function"])
    mock_get_funcs.return_value = mock_df

    result = populate_treatment_dropdown(None, "National", {})
    assert result == []

# Test case: top mode returns a valid chart and no warning message
@patch("callbacks.incomplete_callbacks.get_top_or_bottom_treatments")
def test_update_bar_chart_top_mode(mock_get_top):
    # Simulate DB response for top mode
    mock_df = pd.DataFrame({
        "treatment_function": ["Cardiology", "Gastroenterology"],
        "value": [12.3, 9.7],
    })
    mock_get_top.return_value = mock_df

    # Inputs
    n_clicks = 1
    dummy_trigger = None
    selected_metric = "Average (median) waiting time (in weeks)"
    date_val = "2024-03-01"
    mode = "top"
    selected_codes = None  # ignored in top mode
    selected_granularity = "National"
    selected_region_meta = {"nhs_code": None, "name": None}

    fig, warning = update_bar_chart(
        n_clicks, dummy_trigger, selected_metric, date_val, mode,
        selected_codes, selected_granularity, selected_region_meta
    )

    # The chart should contain data
    assert fig and fig.data
    # No warning message expected
    assert warning == ""


# Test case: manual mode with fewer than 3 selected codes should trigger warning
@patch("callbacks.incomplete_callbacks.get_monthly_treatment_comparison")
def test_update_bar_chart_manual_too_few_selected(mock_get_manual):
    # The query shouldn't be called since validation fails early
    mock_get_manual.return_value = pd.DataFrame()

    n_clicks = 1
    dummy_trigger = None
    selected_metric = "Total number of incomplete pathways"
    date_val = "2024-03-01"
    mode = "manual"
    selected_codes = ["A01"]  # less than 3
    selected_granularity = "Regional"
    selected_region_meta = {"nhs_code": "R123", "name": "Test Region"}

    fig, warning = update_bar_chart(
        n_clicks, dummy_trigger, selected_metric, date_val, mode,
        selected_codes, selected_granularity, selected_region_meta
    )

    # Figure should be empty/default
    assert isinstance(fig, go.Figure)
    # Should display a validation warning
    assert "at least 3 treatment functions" in warning


@patch("callbacks.incomplete_callbacks.get_monthly_treatment_comparison")
def test_update_bar_chart_manual_valid(mock_get_manual):
    # Simulate DB response
    mock_df = pd.DataFrame({
        "treatment_function": ["TF1", "TF2", "TF3", "TF4", "TF5"],
        "value": [10, 12, 8, 15, 9]
    })
    mock_get_manual.return_value = mock_df

    result = update_bar_chart(
        n_clicks=1,
        dummy_trigger=None,
        selected_metric="Total number of incomplete pathways",
        date_val="2024-03-01",
        mode="manual",
        selected_codes=["TF1", "TF2", "TF3", "TF4", "TF5"],
        selected_granularity="Regional",
        selected_region_meta={"nhs_code": "X001", "name": "Some Region"}
    )

    fig, warning = result

    # Should return a figure with data and no warning
    assert isinstance(fig, go.Figure)
    assert len(fig.data) == 5
    assert warning == ""


@patch("callbacks.incomplete_callbacks.get_top_or_bottom_treatments")
def test_update_bar_chart_empty_data(mock_get_top):
    # Simulate empty DB result
    mock_get_top.return_value = pd.DataFrame(columns=["treatment_function", "value"])

    result = update_bar_chart(
        n_clicks=1,
        dummy_trigger=None,
        selected_metric="Total number of incomplete pathways",
        date_val="2024-03-01",
        mode="top",
        selected_codes=None,
        selected_granularity="National",
        selected_region_meta={"nhs_code": None, "name": None}
    )

    fig, warning = result

    assert isinstance(fig, go.Figure)
    assert fig.layout.title.text == "No data available"
    assert warning == ""


def test_toggle_manual_section_manual():
    # When mode is 'manual', section should be shown
    style = toggle_manual_section("manual")
    assert style == {"display": "block"}

def test_toggle_manual_section_non_manual():
    # For any other mode, it should be hidden
    style = toggle_manual_section("top")
    assert style == {"display": "none"}

def test_update_chart_mode_options_known_metric():
    # Use a known metric from your constants
    known_metric = next(iter(METRIC_MODE_LABELS.keys()))
    expected_options = METRIC_MODE_LABELS[known_metric]

    options, default_value = update_chart_mode_options(known_metric)

    assert options == expected_options
    assert default_value == "top"


def test_update_chart_mode_options_unknown_metric():
    # If the metric is not in the mapping, fallback to ['default']
    options, default_value = update_chart_mode_options("Not a real metric")
    assert options == ["default"]
    assert default_value == "top"


def test_update_chart_mode_options_no_metric():
    # Should raise PreventUpdate if metric is None or empty
    with pytest.raises(PreventUpdate):
        update_chart_mode_options(None)

def test_toggle_imd_block_shown():
    # Should be visible only on /incomplete + Regional
    result = toggle_imd_block("Regional", "/incomplete")
    assert result == {"display": "block"}

def test_toggle_imd_block_hidden_wrong_path():
    result = toggle_imd_block("Regional", "/home")
    assert result == {"display": "none"}

def test_toggle_imd_block_hidden_wrong_granularity():
    result = toggle_imd_block("National", "/incomplete")
    assert result == {"display": "none"}


# Test: Regional mode with valid data should return a figure with bars
@patch("callbacks.incomplete_callbacks.get_icb_rtt_for_region_incomplete")
def test_render_icb_rtt_bars_valid(mock_get_rtt):
    # Simulated DB data
    mock_df = pd.DataFrame({
        "org_code": ["ICB01", "ICB02"],
        "org_name": ["NHS ICB One", "NHS ICB Two"],
        "value": [8.1, 12.3],
    })
    mock_get_rtt.return_value = mock_df

    result = render_icb_rtt_bars(
        None,
        "Average (median) waiting time (in weeks)",
        "2024-04-01",
        "ICB02",
        {"nhs_code": "R123"},
        "Regional"
    )

    assert isinstance(result, go.Figure)
    assert len(result.data) > 0
    assert result.data[0].type == "bar"


# Test: National mode or missing region should return an empty figure
@patch("callbacks.incomplete_callbacks.get_icb_rtt_for_region_incomplete")
def test_render_icb_rtt_bars_invalid_context(mock_get_rtt):
    # Even if DB returns data, the chart should not render unless regional
    mock_get_rtt.return_value = pd.DataFrame({
        "org_code": ["ICB01"],
        "org_name": ["NHS ICB One"],
        "value": [9.1]
    })

    result = render_icb_rtt_bars(
        None,
        metric="Total number of incomplete pathways",
        month_value="2024-04-01",
        selected_icb=None,
        region_meta={"nhs_code": "R123"},
        granularity="National"  # Not regional, so chart should not render
    )

    assert isinstance(result, go.Figure)
    # Should be empty since we fallback to empty DF
    assert len(result.data) == 1
    assert result.data[0].type == "bar"
    assert len(result.data[0].x) == 0

# Test: Clear button resets selection, zooms to region, and recolors bars
@patch("callbacks.incomplete_callbacks.get_region_bounds")
@patch("callbacks.incomplete_callbacks._recolor_bars")
def test_select_icb_clear_button(mock_recolor, mock_bounds):
    # Simulate region bounds for map zoom
    mock_bounds.return_value = [[50.0, -2.0], [52.0, 0.0]]  # (s,w),(n,e)
    mock_recolor.return_value = {"data": ["mocked_figure"]}  # simplified dummy figure

    with patch("callbacks.incomplete_callbacks.ctx") as mock_ctx:
        mock_ctx.triggered_id = "incomplete-clear-icb-selection"

        result = select_icb(
            bar_click=None,
            map_click=None,
            clear_clicks=1,
            current_fig={"data": []},
            metric="Total number of incomplete pathways",
            month_value="2024-04-01",
            granularity="Regional",
            region_meta={"nhs_code": "R001"}
        )

        icb_code, center, zoom, selected_fc, fig = result

        # Expected center and zoom calculated from bounds
        assert icb_code is None
        assert center == [51.0, -1.0]  # center of bounds
        assert zoom == 7  # based on span ~2.0 degrees
        assert selected_fc == {"type": "FeatureCollection", "features": []}
        assert fig == {"data": ["mocked_figure"]}


# Test: Clicking bar sets selected ICB and updates map + figure
@patch("callbacks.incomplete_callbacks._recolor_bars")
@patch("callbacks.incomplete_callbacks.get_icb_boundaries_geojson")
def test_select_icb_bar_click(mock_get_geo, mock_recolor):
    # Sample ICB code clicked
    icb_code = "ICB123"

    # Mock the bar clickData from Plotly
    bar_click = {
        "points": [
            {"customdata": [icb_code, "ICB Short", "ICB Full Name"]}
        ]
    }

    # Simulate GeoJSON containing the ICB that matches the click
    mock_get_geo.return_value = {
        "features": [
            {"properties": {"icb_code": icb_code, "center": [53.5, -1.4]}}
        ]
    }

    # Mock recoloring
    mock_recolor.return_value = {"data": ["updated_figure"]}

    with patch("callbacks.incomplete_callbacks.ctx") as mock_ctx:
        mock_ctx.triggered_id = "incomplete-icb-rtt-bars"

        result = select_icb(
            bar_click=bar_click,
            map_click=None,
            clear_clicks=0,
            current_fig={"data": []},
            metric="Average (median) waiting time (in weeks)",
            month_value="2024-04-01",
            granularity="Regional",
            region_meta={"nhs_code": "R999"}
        )

        sel_code, center, zoom, fc, fig = result

        assert sel_code == icb_code
        assert center == [53.5, -1.4]
        assert zoom is no_update  # no zoom change for bar click
        assert fc["features"][0]["properties"]["icb_code"] == icb_code
        assert fig == {"data": ["updated_figure"]}


# Test: Regional mode when no region is selected should show fallback message
def test_render_incomplete_imd_map_invalid():
    # Should show fallback message when granularity is not Regional
    result = render_incomplete_imd_map(
        None,  # dummy input
        granularity="National",
        region_meta={"nhs_code": "R123"}
    )

    assert isinstance(result, html.Div)
    assert "Switch to Regional" in result.children

# Test: Valid Regional mode with mocked data should return map container
@patch("callbacks.incomplete_callbacks.get_region_bounds")
@patch("callbacks.incomplete_callbacks.get_icb_boundaries_geojson")
@patch("callbacks.incomplete_callbacks.get_ccg_imd_geojson")
def test_render_incomplete_imd_map_valid(mock_ccg, mock_icb, mock_bounds):
    # Minimal mocked return values
    mock_ccg.return_value = {"type": "FeatureCollection", "features": []}
    mock_icb.return_value = {"type": "FeatureCollection", "features": []}
    mock_bounds.return_value = [[50.0, -2.0], [52.0, 0.0]]

    result = render_incomplete_imd_map(
        None,  # dummy trigger
        granularity="Regional",
        region_meta={"nhs_code": "R456"}
    )

    # Should return the main map container
    assert isinstance(result, html.Div)
    # Expect a nested dash_leaflet.Map inside
    map_components = [c for c in result.children if isinstance(c, dl.Map)]
    assert len(map_components) == 1

# Test: Simple toggle logic for showing national IMD scatter
def test_toggle_national_imd_block_show():
    result = toggle_national_imd_block("National", "/incomplete")
    assert result == {"display": "block"}

# Test: Should hide for any other granularity or wrong path
def test_toggle_national_imd_block_hide():
    result = toggle_national_imd_block("Regional", "/incomplete")
    assert result == {"display": "none"}

    result = toggle_national_imd_block("National", "/home")
    assert result == {"display": "none"}

# Test: Valid National mode with mocked data should return a scatter figure
@patch("callbacks.incomplete_callbacks.get_icb_imd_scatter_data_incomplete")
@patch("callbacks.incomplete_callbacks.get_national_metric_value_incomplete")
def test_render_national_imd_scatter_valid(mock_nat, mock_icb):
    # Mock main data
    mock_icb.return_value = pd.DataFrame({
        "icb_pop_2019": [100000, 250000],
        "rtt_value": [8.5, 12.1],
        "region_name": ["Region A", "Region B"],
        "imd_quintile": [1, 5],
        "icb_name": ["ICB A", "ICB B"]
    })

    # Mock national average
    mock_nat.return_value = pd.DataFrame({"value": [10.0]})

    result = render_national_imd_scatter(
        metric="Average (median) waiting time (in weeks)",
        month_value="2024-04-01",
        granularity="National"
    )

    assert isinstance(result, go.Figure)
    assert len(result.data) >= 1
    assert result.layout.xaxis.title.text == "Population"

# Test: Empty data should return an empty figure without errors
@patch("callbacks.incomplete_callbacks.get_icb_imd_scatter_data_incomplete")
def test_render_national_imd_scatter_empty(mock_icb):
    # Simulate no data returned
    mock_icb.return_value = pd.DataFrame(columns=["x", "y"])

    result = render_national_imd_scatter(
        metric="Total number of incomplete pathways",
        month_value="2024-04-01",
        granularity="National"
    )

    assert isinstance(result, go.Figure)
    assert len(result.data) == 0  # no trace because no data

# Test: Should return empty figure if granularity is not National
def test_render_national_imd_scatter_wrong_granularity():
    # Should return empty figure if granularity is not National
    result = render_national_imd_scatter(
        metric="Some Metric",
        month_value="2024-04-01",
        granularity="Regional"
    )

    assert isinstance(result, go.Figure)
    assert len(result.data) == 0

# --------------------------------------------------------------------
# open_help_incomplete
# --------------------------------------------------------------------
# Cases:
# - n_clicks falsy -> no_update (do not open / do not change body)
# - n_clicks truthy + National -> True + rendered national help
# - n_clicks truthy + Regional -> True + rendered regional help
from dash import no_update

# open_help_incomplete

@patch.object(icb, "_render_min_help")
def test_open_help_incomplete_no_click(mock_render):
    opened, body = icb.open_help_incomplete(0, "National")
    assert opened is no_update
    assert body is no_update
    mock_render.assert_not_called()


@patch.object(icb, "_render_min_help")
def test_open_help_incomplete_national(mock_render):
    # Patch the constant where it is used
    with patch.object(icb, "PAGE_HELP_MIN",
                      {"incomplete_national": {"k": "v"}, "incomplete_regional": {"x": "y"}}):
        mock_render.return_value = "rendered-national"
        opened, body = icb.open_help_incomplete(1, "National")
        assert opened is True
        assert body == "rendered-national"
        mock_render.assert_called_once_with({"k": "v"})


@patch.object(icb, "_render_min_help")
def test_open_help_incomplete_regional(mock_render):
    with patch.object(icb, "PAGE_HELP_MIN",
                      {"incomplete_national": {"k": "v"}, "incomplete_regional": {"x": "y"}}):
        mock_render.return_value = "rendered-regional"
        opened, body = icb.open_help_incomplete(2, "Regional")
        assert opened is True
        assert body == "rendered-regional"
        mock_render.assert_called_once_with({"x": "y"})


# --------------------------------------------------------------------
# update_metric_help
# --------------------------------------------------------------------
# Cases:
# - None metric -> no_update
# - Metric not in INCOMPLETE_DROPDOWN_MAP -> no_update
# - Metric in map -> returns build_help_icon(text) where text from METRIC_HELP_TEXT["incomplete"][key]

def test_update_metric_help_none():
    assert update_metric_help(None) is no_update

@patch.object(icb, "INCOMPLETE_DROPDOWN_MAP", {})
def test_update_metric_help_not_mapped():
    # No mapping means the metric isn't recognized; callback should not update the UI
    assert icb.update_metric_help("Unmapped Metric") is no_update


@patch.object(icb, "build_help_icon")
def test_update_metric_help_mapped(mock_build):
    # Provide minimal, controlled mappings on the module so the callback
    # reads our test data instead of real constants.
    with patch.object(icb, "INCOMPLETE_DROPDOWN_MAP", {"Known Metric": "known_key"}), \
         patch.object(icb, "METRIC_HELP_TEXT", {"incomplete": {"known_key": "help text here"}}):
        mock_build.return_value = "HELP_ICON"

        result = icb.update_metric_help("Known Metric")

        # Should render the help icon from the mapped help text
        assert result == "HELP_ICON"
        mock_build.assert_called_once_with("help text here")


# --------------------------------------------------------------------
# update_regional_subtitle
# --------------------------------------------------------------------
# Cases:
# - Wrong granularity or missing month -> ""
# - Valid inputs -> formatted string contains metric, month label, region name

def test_update_regional_subtitle_wrong_context():
    # Not Regional
    assert update_regional_subtitle("m", "2024-03-01", "National", {"name": "X"}) == ""
    # Missing month
    assert update_regional_subtitle("m", None, "Regional", {"name": "X"}) == ""


def test_update_regional_subtitle_ok():
    text = update_regional_subtitle(
        "Average (median) waiting time (in weeks)",
        "2024-03-01",
        "Regional",
        {"name": "North East"}
    )
    assert "Average (median) waiting time (in weeks)" in text
    assert "March 2024" in text
    assert "North East" in text
    assert "map and bar chart" in text


# --------------------------------------------------------------------
# update_national_subtitle
# --------------------------------------------------------------------
# Cases:
# - Wrong granularity or missing month -> ""
# - Valid -> formatted string contains metric + month

def test_update_national_subtitle_wrong_context():
    assert update_national_subtitle("m", "2024-03-01", "Regional") == ""
    assert update_national_subtitle("m", None, "National") == ""


def test_update_national_subtitle_ok():
    text = update_national_subtitle(
        "Total number of incomplete pathways",
        "2024-04-01",
        "National"
    )
    assert "Total number of incomplete pathways" in text
    assert "April 2024" in text
    assert "deprivation and population" in text


# --------------------------------------------------------------------
# update_incomplete_title
# --------------------------------------------------------------------
# Cases:
# - National -> national title text
# - Regional -> includes region name

def test_update_incomplete_title_national():
    title = update_incomplete_title("National", {"name": "Ignored"})
    assert "National Overview" in title
    assert "Incomplete RTT Pathways" in title


def test_update_incomplete_title_regional():
    title = update_incomplete_title("Regional", {"name": "South East"})
    assert "Regional Overview: South East" in title
    assert "Incomplete RTT Pathways" in title








