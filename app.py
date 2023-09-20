from dash import Dash, html, dcc, Input, Output, callback, State
from data import generate_data, min_year, max_year, year_values
from map import generate_map
import json


import dash_bootstrap_components as dbc

import plotly.express as px

from pdb import set_trace

def as_mark_dic(arr, prefix=""):
    "Generate dict to be passed to step parameter on RangeSlider"
    return_dic = {}
    [return_dic.update({str(e): prefix + str(e)}) for e in arr]
    return return_dic

app = Dash(__name__, external_stylesheets=[dbc.themes.CYBORG])

app.layout = html.Div(
    dbc.Container([
        dbc.Stack([
            dbc.Row([
                dbc.Col(
                    html.P("Intervalo de tempo a ser filtrado:"),
                    width='auto'
                ),
            ]),
            dbc.Row(
                dbc.Col(
                    dcc.RangeSlider(min_year, max_year, value=[min_year, max_year],
                                    step=None, id="year_interval_slider", marks=as_mark_dic(year_values),
                                    className="year_interval_slider"),
                )
            ),

        dbc.Row([
            dbc.Col(
                dbc.Button("Resetar", id="reset-buttom", n_clicks=0),
                width='auto'
            ),
            dbc.Col(
                html.P("Valores mínimo e máximo para filtrar:"),
                width='auto'
            ),
        ]),
            dbc.Row(
                dbc.Col(
                    dcc.RangeSlider(0, 1000000000, value=[0,1000000000], id="value_range_slider", included=True,
                                    tooltip={'always_visible':True, 'placement': 'bottom'}),
                )
            ),

        dbc.Row(dcc.Dropdown(id="bairros-multi-dropdown", multi=True, placeholder="Filtre por bairros")),

        dbc.Row(
            html.Div([
                dcc.Graph(figure={}, id="the_map"),
            ]),
        ),

        dcc.Store("bairros_colors_store"),
            dcc.Store("min-max-val"),
        ], gap=2)
    ])
)

@callback(
    Output("value_range_slider", "min"),
    Output("value_range_slider", "max"),
    Output("value_range_slider", "value"),
    Input("min-max-val", "data"),
    prevent_initial_call=True
)
def update_value_slider(min_max_val):
    data = json.loads(min_max_val)
    min_val, max_val = min(data) - 1, max(data) + 1
    return min_val, max_val, (min_val, max_val)

@callback(
    Output("bairros-multi-dropdown", "options"),
    Input("bairros_colors_store", "data"),
    prevent_initial_call=True
    )
def update_bairros_checklist(data):
    data = json.loads(data)
    options = [{"label": html.Div([n], style={'color': data[n]}), "value": n} for n in data.keys()]
    value = [e['value'] for e in options]
    return options


@callback(
    Output("year_interval_slider", "value"),
    Output("value_range_slider", "value", allow_duplicate=True),
    Input("reset-buttom", "n_clicks"),
    prevent_initial_call=True
    )
def reset_by_year_interval(value):
    return (min_year, max_year), None

@callback(
    Output("the_map", "figure"),
    Output("min-max-val", "data"),
    Output("bairros_colors_store", "data"),
    Input("year_interval_slider", "value"),
    State("value_range_slider", "value"),
    Input("bairros-multi-dropdown", "value")
)
def generate_graph(year, value, bairros_to_include):
    data = generate_data(
        year_interval=year,
        total_value_interval=value,
        bairros_to_include=bairros_to_include
    )

    map = generate_map(data[0], data[2])

    return map[0],  json.dumps(list(data[1])), json.dumps(map[1])

@callback(
    Output("the_map","figure", allow_duplicate=True),
    Output("bairros_colors_store", "data", allow_duplicate=True),
    State("year_interval_slider", "value"),
    Input("value_range_slider", "value"),
    State("bairros-multi-dropdown", "value"),
    prevent_initial_call=True
)
def generate_graph_filter_by_value(year, min_max, bairros):
    data = generate_data(
        year_interval=year,
        total_value_interval=min_max,
        bairros_to_include=bairros
    )

    map = generate_map(data[0], data[2])

    return map[0], json.dumps(map[1])


if __name__ == '__main__':
    app.run(debug=True)
