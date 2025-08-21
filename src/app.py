# app.py
from dash import Dash, html, dcc, Input, Output
import dash_bootstrap_components as dbc
import dash_mantine_components as dmc 

from layouts.incomplete_layout import incomplete_layout
from layouts.admitted_layout import admitted_layout
from layouts.non_admitted_layout import non_admitted_layout
from layouts.new_referrals_layout import new_referrals_layout
from layouts.home_layout import home_layout
from layouts.help_layout import help_layout

import callbacks.admitted_callbacks 
import callbacks.non_admitted_callbacks 
import callbacks.new_callbacks 
import callbacks.incomplete_callbacks 
import callbacks.home_callbacks
import callbacks.shared_callbacks
import plotly.io as pio

# Apply a global font + optional colors
pio.templates.default = "plotly_white"
pio.templates["plotly_white"].layout.font.family = "Inter, Segoe UI, Roboto, sans-serif"
pio.templates["plotly_white"].layout.font.size = 14
pio.templates["plotly_white"].layout.title.font.size = 16

pio.templates["plotly_white"].layout.update({
    "font": {"family": "Inter, Segoe UI, Roboto, sans-serif", "size": 14},
    "title": {"font": {"size": 18, "family": "Inter, Segoe UI, Roboto, sans-serif"}},
    "paper_bgcolor": "white",     # keep overall card/page background white
    "plot_bgcolor": "#f7f9fc",    # light grey-blue to define the chart area
    "xaxis": {"gridcolor": "#e9eef5", "zeroline": False, "automargin": True},
    "yaxis": {"gridcolor": "#e9eef5", "zeroline": False, "automargin": True},
})

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="NHS RTT Dashboard",
)

# Global theme + global container for all pages
import dash_mantine_components as dmc

app.layout = dmc.MantineProvider(
    withCssVariables=True,            
    withGlobalClasses=True,           
    theme={
        "fontFamily": "Inter, Segoe UI, Roboto, system-ui, sans-serif",
        "colors": {
            "nhsblue": [
                "#e6f0fa","#cde1f6","#9fc3ec","#74a6e2","#4b89d8",
                "#2563eb","#1f53c9","#1842a1","#123279","#0c2252"
            ],
        },
        "primaryColor": "nhsblue",
        "headings": {
            "fontFamily": "Inter, Segoe UI, Roboto, system-ui, sans-serif",
            "sizes": {
                "h1": {"fontSize": "28px", "fontWeight": 800},
                "h2": {"fontSize": "24px", "fontWeight": 700},
                "h3": {"fontSize": "20px", "fontWeight": 700},
            },
        },
    },
    children=html.Div([
        dcc.Location(id='url', refresh=False),
        dcc.Store(id='selected-region-meta', storage_type='session'),
        dcc.Store(id="selected-granularity", storage_type="session"),
        html.Div(id='page-content')
    ])
)


# Routing
@app.callback(Output('page-content', 'children'), Input('url', 'pathname'))
def display_page(pathname):
    if pathname == "/admitted":
        return admitted_layout
    elif pathname == "/non-admitted":
        return non_admitted_layout
    elif pathname == "/new-referrals":
        return new_referrals_layout
    elif pathname == "/incomplete":
        return incomplete_layout
    elif pathname == "/help":
        return help_layout
    return home_layout


if __name__ == "__main__":
    print("Launching multi-page NHS dashboard...")
    app.run(debug=True)
