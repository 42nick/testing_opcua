import dash
import dash_bootstrap_components as dbc
from dash import Input, Output, dcc, html

from testing_opcua.client import connect_and_get_values
from testing_opcua.figure_creation import get_gauge_chart
from testing_opcua.shared import get_ip

app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])
import plotly.graph_objects as go


class IDs:
    BUTTON = "BUTTON"
    P_LIVE = "P_LIVE"

    GRAPH_LIVE_TEMP = "GRAPH_LIVE_TEMP"
    GRAPH_LIVE_HUMIDITY = "GRAPH_LIVE_HUMIDITY"

    INTERVAL = "INTERVAL"


# the style arguments for the sidebar. We use position:fixed and a fixed width
SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "18rem",
    "padding": "2rem 1rem",
    "background-color": "#f8f9fa",
}

# the styles for the main content position it to the right of the sidebar and
# add some padding.
CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Raspberry Pi Dashboard", className="display-4"),
        html.Hr(),
        dbc.Nav(
            [
                dbc.NavLink("Live Temperature", href="/", active="exact"),
                dbc.NavLink("Temperature History", href="/page-1", active="exact"),
                dbc.NavLink("Settings", href="/page-2", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE,
)

content = html.Div(id="page-content", style=CONTENT_STYLE)


app.layout = html.Div(
    [
        dcc.Location(id="url"),
        sidebar,
        content,
        dcc.Interval(id=IDs.INTERVAL, interval=1 * 1000, n_intervals=0),  # in milliseconds
    ]
)

page_live_temp = html.Div(
    [
        dbc.Col(html.P("Temperature and humidity at currently no time.", id=IDs.P_LIVE)),
        dbc.Col(html.Div([dcc.Graph(id=IDs.GRAPH_LIVE_TEMP)])),
        dbc.Col(html.Div([dcc.Graph(id=IDs.GRAPH_LIVE_HUMIDITY)])),
    ]
)


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return page_live_temp
    elif pathname == "/page-1":
        return html.P("This is the content of page 1. Yay!")
    elif pathname == "/page-2":
        return html.P("There are no settings yet!")
    # If the user tries to reach a different page, return a 404 message
    return dbc.Jumbotron(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ]
    )


# Multiple components can update everytime interval gets fired.
@app.callback(
    [
        Output(IDs.GRAPH_LIVE_TEMP, "figure"),
        Output(IDs.GRAPH_LIVE_HUMIDITY, "figure"),
    ],
    Input(IDs.INTERVAL, "n_intervals"),
)
def update_graph_live(n):

    time, temp, humidity = connect_and_get_values()

    return get_gauge_chart(temp, "Temperature in °C"), get_gauge_chart(humidity, "Humidiy in %")


if __name__ == "__main__":
    try:
        app.run_server(host=get_ip(), port=8888)
    except OSError:
        app.run_server(host="127.0.0.1", port=8888, debug=True)
