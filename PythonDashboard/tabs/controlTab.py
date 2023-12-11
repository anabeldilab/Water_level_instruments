from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

def control_auto_tab():
    return html.Div([
        html.H3("Control Automático", className="text-center mb-4"),

        # Selección del sensor
        dbc.Row([
            dbc.Col([
                html.Label("Selección del Sensor"),
                dcc.Dropdown(
                    id="sensor-dropdown",
                    options=[
                        {"label": "Báscula", "value": "bascula"},
                        {"label": "Condensador", "value": "condensador"}
                    ],
                    value="bascula"
                ),
            ], width=6),

            # Fijación de consigna
            dbc.Col([
                html.Label("Fijación de Consigna"),
                dcc.Input(id="consigna-input", type="number", placeholder="Consigna", className="form-control"),
            ], width=6),
        ], className="mb-3"),

        # Sintonización de parámetros del controlador
        dbc.Row([
            dbc.Col([
                html.Label("Sintonización de Parámetros del Controlador"),
                dcc.Input(id="parametros-controlador", type="number", placeholder="Parámetro", className="form-control"),
            ], width=12),
        ], className="mb-3"),

        # Representación del nivel real, consigna y error de control
        dbc.Row([
            dbc.Col([
                dcc.Graph(id="control-graph"),
            ], width=8),

            dbc.Col([
                daq.Tank(
                    id='my-tank-1',
                    color='#1c1cd4',
                    height=400,
                    width=200,
                    value=50,
                    min=0,
                    max=100,
                    label='Nivel de agua',
                ),
            ], width=4),  # Adjust the width as needed
        ])
    ])
