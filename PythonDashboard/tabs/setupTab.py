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
                        dbc.Button("Llenar Tanque", id="boton-llenar", color="success", className="me-2"),
                        html.Div(id="indicador-llenar", style={"height": "10px"}),  # Indicador para 'Llenar Tanque'
                        dbc.Button("Vaciar Tanque", id="boton-vaciar", color="warning", className="me-2"),
                        html.Div(id="indicador-vaciar", style={"height": "10px"}),  # Indicador para 'Vaciar Tanque'
                        dbc.Button("Parar Bomba", id="boton-parar", color="danger"),
                    ])
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Control de la Báscula", className="card-title"),
                        dbc.Button("Tarar Báscula", id="boton-tarar", color="primary", className="me-2"),
                        dbc.Button("Escalar Báscula", id="boton-escalar", color="secondary"),
                    ])
                ], className="mb-3"),
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Frecuencia de Circuito RC", className="card-title"),
                        dcc.Input(id="input-frecuencia", type="number", placeholder="Ingresar Frecuencia", className="form-control"),
                    ])
                ], className="mb-3"),
            ]),
            dbc.Col(width=6, children=[
                dbc.Card([
                    dbc.CardBody([
                        html.H5("Medidas", className="card-title", style={"text-align": "center"}),
                        html.Div(id="indicador-medidas"),
                        dash_table.DataTable(
                            id='tabla-medidas',
                            columns=[
                                {"name": "Medida", "id": "medida"},
                                {"name": "Valor", "id": "valor"}
                            ],
                            data=[
                                {"medida": "Peso de la Báscula (g)", "valor": ""},
                                {"medida": "Medida Circuito RC", "valor": ""},
                                {"medida": "Peso según Circuito RC", "valor": ""}
                            ],
                            style_table={'overflowX': 'auto'},
                            style_cell={'textAlign': 'center'},
                            style_data={'backgroundColor': 'rgb(50, 50, 50)', 'color': 'white', 'border': '1px white solid'},
                            style_header={'backgroundColor': 'rgb(30, 30, 30)', 'fontWeight': 'bold', 'border': '1px white solid'}
                        )
                    ])
                ]),
            ]),
        ]),
    ])
