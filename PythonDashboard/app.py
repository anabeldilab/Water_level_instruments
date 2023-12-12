import dash
import dash_bootstrap_components as dbc
from dash import callback, Output, Input, ctx
from tabs import setupTab
from tabs import calibrationRCTab
from tabs import controlTab
from SCPI_Control import SCPI_Arduino

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(setupTab.setup_tab(), label="Setup"),
        dbc.Tab(calibrationRCTab.calibration_tab(), label="Calibración RC"),
        dbc.Tab(controlTab.control_auto_tab(), label="Control automático"),
    ]),
], fluid=True)

@callback(
    [Output("indicador-llenar", "style"),
     Output("indicador-vaciar", "style")],
    [Input("boton-llenar", "n_clicks"),
     Input("boton-vaciar", "n_clicks"),
     Input("boton-parar", "n_clicks")]
)
def update_indicators(btn_llenar, btn_vaciar, btn_parar):
    style_on = {"height": "10px", "background-color": "green"}
    style_off = {"height": "10px", "background-color": "transparent"}

    # Si se presiona 'Parar Bomba', apaga todos los indicadores
    if "boton-parar" == ctx.triggered_id:
        SCPI_Arduino('STOP')
        return style_off, style_off

    # Cambia el estilo del indicador según el botón presionado
    if "boton-llenar" == ctx.triggered_id:
        SCPI_Arduino('INC')
        return style_on, style_off
    elif "boton-vaciar" == ctx.triggered_id:
        SCPI_Arduino('DEC')
        return style_off, style_on

    # Estado inicial (todo apagado)
    return style_off, style_off

@callback(
    Output("indicador-medidas", "children"),
    [Input("boton-tarar", "n_clicks"),
     Input("boton-escalar", "n_clicks")]
)
def scale_control(btn_tarar, btn_escalar):
    if "boton-tarar" == ctx.triggered_id:
        SCPI_Arduino('TARE')
    elif "boton-escalar" == ctx.triggered_id:
        SCPI_Arduino('CHANGEUNITS')

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)