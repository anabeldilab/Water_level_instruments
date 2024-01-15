from dash import html, dcc
import dash_bootstrap_components as dbc
import dash_daq as daq

def control_auto_tab():
    return html.Div([
        html.H3("Control Automático", className="text-center mb-4"),

        dbc.Row([ 
            dbc.Col([
                dbc.Row([
                    html.Label("Selección del Sensor"),
                    dcc.Dropdown(
                        id="sensor-dropdown",
                        options=[
                            {"label": "Báscula", "value": "bascula"},
                            {"label": "Condensador", "value": "condensador"}
                        ],
                        value="bascula",
                        clearable=False,
                        style={'color': 'black'}
                    ),
                ], style={"margin-bottom": "60px", "margin-left": "20px", "margin-right": "20px",}),
                dbc.Row([ 
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
            dbc.Col([
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
                                'data': [
                                    {'time': [], 'weight': []}
                                ],
                                'layout': {
                                    'xaxis': {'title': 'Tiempo (s)'},
                                    'yaxis': {'title': 'Peso'},
                                }
                            },
                            config={
                                'staticPlot': True,
                                'displayModeBar': False 
                            }
                        ),
                    ], width=9),
                ], className="mb-3", style={"margin-bottom": "10px"}),
                dbc.Row([
                    dbc.Col([
                        html.Label("Consigna actual:"),
                        dcc.Markdown(
                            id="current_setpoint", 
                            children="", 
                            style={
                                'backgroundColor': 'white', 
                                'textAlign': 'center',
                                'color': 'black',
                                'height': '70px',
                                'borderRadius': '15px',
                                'padding': '10px',
                                'overflowY': 'auto'
                            })
                    ], width=4),

                    dbc.Col([
                        html.Label("Peso actual:"),
                        dcc.Markdown(
                            id="current_weight", 
                            children="", 
                            style={
                                'backgroundColor': 'white', 
                                'textAlign': 'center',
                                'color': 'black',
                                'height': '70px',
                                'borderRadius': '15px',
                                'padding': '10px',
                                'overflowY': 'auto'
                            })
                    ], width=4),

                    dbc.Col([
                        html.Label("Error actual:"),
                        dcc.Markdown(
                            id="current_error", 
                            children="", 
                            style={
                                'backgroundColor': 'white', 
                                'textAlign': 'center',
                                'color': 'black',
                                'height': '70px',
                                'borderRadius': '15px',
                                'padding': '10px',
                                'overflowY': 'auto'
                            })
                    ], width=4)
                ])  
            ]), 
        ]),
    ])