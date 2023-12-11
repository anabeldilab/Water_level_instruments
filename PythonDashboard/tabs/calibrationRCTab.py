from dash import html, dcc
from dash import dash_table
import dash_bootstrap_components as dbc

def calibration_tab():
    return html.Div([
        html.H3("Calibración", className="text-center mb-4"),

        dbc.Row([
            dbc.Col([
                dbc.Button("Run", id="calib-run-button", color="success", className="me-2"),
                dbc.Button("Stop", id="calib-stop-button", color="danger", className="me-2"),
                dcc.Input(id="calib-sample-size", type="number", placeholder="Número de Muestras", className="form-control"),
            ], width=12)
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dcc.Graph(id="calib-graph"),
            ], width=12)
        ], className="mb-3"),

        dbc.Row([
            dbc.Col([
                dash_table.DataTable(
                    id='calib-table',
                    columns=[{"name": "Muestra", "id": "Muestra"}, {"name": "Valor", "id": "Valor"}],
                    data=[],
                )
            ], width=12)
        ])
    ])