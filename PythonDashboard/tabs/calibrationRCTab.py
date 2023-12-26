from dash import html, dcc
from dash import dash_table
import dash_bootstrap_components as dbc

def calibration_tab():
    return html.Div([
        html.H3("Calibración", className = "text-center mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Button("Run", id = "calib-run-button", color = "success", className = "me-2"),
                dbc.Button("Stop", id = "calib-stop-button", color = "danger", className = "me-2"),
                html.Div(style = {"height": "10px"}),
                dcc.Input(id = "calib-sample-size", type = "number", placeholder = "Número de Muestras", className = "form-control"),
            ], width = 12)
        ], className = "mb-3"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(
                    id = "calib-graph",
                    figure = {
                        'data': [],
                        'layout': {
                            'title': 'Circuito RC vs. Báscula',
                            'xaxis': {'title': 'Peso Báscula (g)'},
                            'yaxis': {'title': 'Medida Circuito RC'},
                        }
                    }
                ),
            ], width = 7),

            dbc.Col([ 
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Graph Units", className = "card-title", style = {"text-align": "center"}),
                        html.Div(id = "graph-units-indicator"),
                        dash_table.DataTable(
                            id = 'graph-units-table',
                            columns = [
                                {"name": "Measure", "id": "measure"},
                                {"name": "Value", "id": "value"}
                            ],
                            data = [
                                {"medida": "Peso de la Báscula (g)", "valor": ""},
                                {"medida": "Medida Circuito RC", "valor": ""},
                                {"medida": "Peso según Circuito RC", "valor": ""}
                            ],
                            style_table = {'overflowX': 'auto'},
                            style_cell = {'textAlign': 'center'},
                            style_data = {'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white', 'border': '1px white solid'},
                            style_header = {'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold', 'border': '1px white solid'},
                            cell_selectable = False
                        )
                    ])
                ]),
            ], width = 5) 
        ], className = "mb-3"),
    ])
