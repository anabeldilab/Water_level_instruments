from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

def control_auto_tab():
    return html.Div([
        html.H3("Control Automático", className="text-center mb-4"),

        dbc.Row([  # Una sola fila para todas las columnas
            dbc.Col([  # Columna para Selección del Sensor y Fijación de Consigna
                dbc.Row([  # Subfila para Selección del Sensor
                    html.Label("Selección del Sensor"),
                    dcc.Dropdown(
                        id="sensor-dropdown",
                        options=[
                            {"label": "Báscula", "value": "bascula"},
                            {"label": "Condensador", "value": "condensador"}
                        ],
                        value="bascula",
                        style={'color': 'black'}
                    ),
                ], style={"margin-bottom": "60px", "margin-left": "20px", "margin-right": "20px",}),
                dbc.Row([  # Subfila para Fijación de Consigna
                    html.Label("Fijación de Consigna"),
                    dcc.Input(id="consigna-input", type="number", placeholder="Consigna", className="form-control"),
                ], style={"margin-bottom": "60px", "margin-left": "20px", "margin-right": "20px"}),
                dbc.Row([
                    html.Label("Sintonización de Parámetros del Controlador"),
                    dcc.Input(id="parametros-controlador", type="number", placeholder="Parámetro", className="form-control"),
                ], style={"margin-bottom": "60px", "margin-left": "20px", "margin-right": "20px"}),
               dbc.Row([
                    dbc.Button("Run", id="control-run-button", color="success", className="me-2"),
                    html.Div(style = {"height": "10px"}),
                    dbc.Button("Stop", id="control-stop-button", color="danger", className="me-2"),
                ], style={"margin-bottom": "30px", "margin-left": "20px", "margin-right": "20px"}),
            ], width=4),
            dbc.Col([  # Columna para Indicadores de Estado
                dbc.Row([
                    dbc.Col([
                        html.Div([
                            daq.Tank(
                                id='my-tank-1',
                                color='#1c1cd4',
                                height=400,
                                #width=200,
                                value=50,
                                min=0,
                                max=100,
                                label='Nivel de agua',
                            ),
                        ], style={'color': 'white'}),   
                    ], width=3),
                    dbc.Col([
                        dcc.Graph(
                            id = "control-graph",
                            figure = {
                                'data': [],
                                'layout': {
                                    'xaxis': {'title': 'Tiempo (s)'},
                                    'yaxis': {'title': 'Peso'},
                                }
                            },
                            config={
                                'staticPlot': True,  # Deshabilita zoom, paneo, etc.
                                'displayModeBar': False  # Oculta la barra de herramientas del gráfico
                            }
                        ),
                    ], width=9),
                ], className="mb-3", style={"margin-bottom": "10px"}),
                dbc.Row([  # Subfila para mostrar datos
                    dbc.Col([
                        html.Label("Datos del Sistema"),
                        dcc.Input(id="datos-sistema", type="number", placeholder="Datos", className="form-control"),
                    ]),
                ]),
                    
            ]), 
        ]),
    ])
