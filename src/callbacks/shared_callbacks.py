from dash import callback, Output, Input, State, no_update
from dash.exceptions import PreventUpdate
from dash import ctx



@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("selected-granularity", "data", allow_duplicate=True),
    Output("selected-region-meta", "data", allow_duplicate=True),
    Input("back-home-btn", "n_clicks"),
    prevent_initial_call=True
)
def handle_back_to_home(n_clicks):
    
    if ctx.triggered_id != "back-home-btn":
        raise PreventUpdate

    if not n_clicks:
        raise PreventUpdate
    
    return "/", None, None


@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("selected-granularity", "data", allow_duplicate=True),
    Output("selected-region-meta", "data", allow_duplicate=True),
    Input("back-home-btn-admitted", "n_clicks"),
    prevent_initial_call=True
)
def handle_back_to_home_admitted(n_clicks):
    
    if ctx.triggered_id != "back-home-btn-admitted":
        raise PreventUpdate

    if not n_clicks:
        raise PreventUpdate
    

    return "/", None, None

@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("selected-granularity", "data", allow_duplicate=True),
    Output("selected-region-meta", "data", allow_duplicate=True),
    Input("back-home-btn-non-admitted", "n_clicks"),
    prevent_initial_call=True
)
def handle_back_to_home_non_admitted(n_clicks):
    
    if ctx.triggered_id != "back-home-btn-non-admitted":
        raise PreventUpdate

    if not n_clicks:
        raise PreventUpdate


    return "/", None, None



@callback(
    Output("url", "pathname", allow_duplicate=True),
    Output("selected-granularity", "data", allow_duplicate=True),
    Output("selected-region-meta", "data", allow_duplicate=True),
    Input("back-home-btn-new", "n_clicks"),
    prevent_initial_call=True
)
def handle_back_to_home_new(n_clicks):
    
    if ctx.triggered_id != "back-home-btn-new":
        raise PreventUpdate

    if not n_clicks:
        raise PreventUpdate


    return "/", None, None

