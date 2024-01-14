from dash import html, dcc
from dash import dash_table
import dash_bootstrap_components as dbc

def calibration_tab():
    return html.Div([
        html.H3("Calibración", className = "text-center mb-4"),
        html.Div(id='update-complete-flag', style={'display': 'none'}),
        dbc.Row([
            dbc.Col([
                dbc.Button("Run", id = "calib-run-button", color = "success", className = "me-2"),
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
                    },
                    config={
                        'staticPlot': True,
                        'displayModeBar': False
                    }
                ),
            ], width = 7),

            dbc.Col([ 
                dbc.Row([
                    dbc.Card([
                        dbc.CardBody([
                            html.H5("Graph Units", className = "card-title", style = {"text-align": "center"}),
                            html.Div(id = "graph-units-indicator"),
                            dash_table.DataTable(
                                id = 'graph-units-table',
                                columns = [
                                    {"name": "Peso", "id": "weight"},
                                    {"name": "RC", "id": "rc-value"}
                                ],
                                data = [
                                    {"weight": "", "rc-value": ""},
                                    {"weight": "", "rc-value": ""},
                                    {"weight": "", "rc-value": ""}
                                ],
                                style_table = {'overflowX': 'auto'},
                                style_cell = {'textAlign': 'center'},
                                style_data = {'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white', 'border': '1px white solid'},
                                style_header = {'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold', 'border': '1px white solid'},
                                cell_selectable = False
                            )
                        ])
                    ]),
                ], className = "mb-3"),
                dbc.Row([
                    dbc.Button("Ajuste", id = "calib-adjust-button", color = "success", className = "me-2"),
                ], className = "mb-3", style = {
                        'margin-top': '10px',
                        'margin-right': '10px',
                        'margin-bottom': '10px',
                        'margin-left': '10px',
                    }),
                dbc.Modal([
                    dbc.ModalBody("Calibrando..."),
                    dbc.ModalFooter(dbc.Button("Stop", id = "close-modal", color = "danger",  className = "me-2", n_clicks = 0)),
                ], id = "calibration-modal", is_open = False),
            ], width = 5)
        ], className = "mb-3"),
    ])
