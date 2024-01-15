from dash import html, dcc, dash_table
import dash_bootstrap_components as dbc

def setup_tab():
    return html.Div([
        html.H3("Setup del Sistema", className="text-center mb-4"),
        dbc.Row([
            dbc.Col(width=6, children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Control de Bombas", className="card-title"),
                        dbc.Button("Llenar Tanque", id="boton-llenar", color="success", className="me-2 w-100", style={"border": "5px solid transparent", "border-radius": "5px"}),
                        html.Div(style={"margin-bottom": "10px"}),
                        dbc.Button("Vaciar Tanque", id="boton-vaciar", color="warning", className="me-2 w-100", style={"border": "5px solid transparent", "border-radius": "5px"}),
                        html.Div(style={"margin-bottom": "10px"}),
                        dbc.Button("Parar Bomba", id="boton-parar", color="danger", className="me-2 w-100"),
                    ])
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Control de la Báscula", className="card-title"),
                        dbc.Col(dbc.Button("Tarar Báscula", id="boton-tarar", color="primary", className="me-2 w-100"), className="mb-3"),
                        dbc.Col(dbc.Button("Escalar Báscula", id="boton-escalar", color="secondary", className="me-2 w-100"), className="mb-3"),
                        dbc.Modal(
                            [
                                dbc.ModalHeader(dbc.ModalTitle("Escalar Báscula")),
                                dbc.ModalBody([
                                    html.P("Ponga un peso conocido en la báscula."),
                                    html.P(" Luego, ingrese el valor de dicho peso en gramos en el campo de texto y presione el botón de \"Escalar\"."),
                                    dcc.Input(id="input-escalado", type="number", placeholder="Valor de Escalado", className="me-2"),
                                ]),
                                dbc.ModalFooter(
                                    dbc.Button("Escalar Báscula", id="boton-guardar-escalado", className="ms-auto", color="primary"),
                                    style={"display": "flex", "justifyContent": "center"}
                                ),
                            ],
                            id="modal-escalar",
                            is_open=False,
                        ),
                        html.Label("Máximo de Peso:", className="mt-3"),
                        dbc.Row([
                            dbc.Col(
                                dcc.Input(
                                    id="input-max-peso", 
                                    type="number", 
                                    placeholder="Máximo Peso", 
                                    className="form-control", 
                                    style={"-moz-appearance": "textfield", "appearance": "textfield"}
                                ), 
                                width=10
                            ),
                            dbc.Col(
                                dbc.Button("Establecer Máximo", id="boton-max-peso", color="primary", className="ms-2"), 
                                width=2
                            ),
                        ], className="mt-3 align-items-center"),
                    ])
                ], className="mb-3"),
            ]),
            dbc.Col(width=6, children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Current Units", className="card-title", style={"text-align": "center"}),
                        html.Div(id="current-units-indicator"),
                        dash_table.DataTable(
                            id='current-units-measures',
                            columns=[
                                {"name": "Measure", "id": "measure"},
                                {"name": "Value", "id": "value"}
                            ],
                            data=[
                                {"measure": "Peso de la Báscula (g)", "value": ""},
                                {"measure": "Medida Circuito RC", "value": ""},
                                {"measure": "Peso según Circuito RC", "value": ""}
                            ],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'center'},
                            style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white', 'border': '1px white solid'},
                            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold', 'border': '1px white solid'},
                            cell_selectable=False
                        )
                    ])
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Frecuencia de Circuito RC", className="card-title"),
                        dbc.Row([
                            dbc.Col(
                                dcc.Input(
                                    id="input-frecuencia", 
                                    type="number", 
                                    placeholder="Ingresar Frecuencia", 
                                    className="form-control",
                                    style={"-moz-appearance": "textfield", "appearance": "textfield"}
                                ),
                                width=10
                            ),
                            dbc.Col(
                                dbc.Button("Enviar", id="boton-send-freqrc", color="primary", className="ms-2"),
                                width=2
                            ),
                        ], align="center"),
                    ])
                ], className="mb-3"),
            ]),
        ]),
    ])
