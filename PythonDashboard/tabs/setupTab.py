from dash import html, dcc
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
                        dbc.Button("Vaciar Tanque", id="boton-vaciar", color="warning", className="me-2"),
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
                        html.H5("Indicadores de Medidas", className="card-title"),
                        html.Div(id="indicador-medidas"),
                    ])
                ]),
            ]),
        ]),
    ])
