import dash
import dash_bootstrap_components as dbc
from dash import callback, Output, Input, ctx, dcc
from tabs import setupTab
from tabs import calibrationRCTab
from tabs import controlTab
from concurrent.futures import ThreadPoolExecutor
from SCPI_Control import SCPI_Arduino
from redpitaya_instrument import RC_circuit_value
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])

calibrationList = []

app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(setupTab.setup_tab(), label = "Setup", tab_id = 'tab-1'),
        dbc.Tab(calibrationRCTab.calibration_tab(), label = "Calibración RC", tab_id = 'tab-2'),
        dbc.Tab(controlTab.control_auto_tab(), label = "Control automático", tab_id = 'tab-3'),
    ], id = 'tabs', active_tab = 'tab-1'),
    dcc.Interval(
        id = 'interval-setup',
        interval = 3*1000, # in milliseconds
        n_intervals = 0,
        max_intervals = -1
    ),
    dcc.Interval(
        id = 'interval-calibration',
        interval = 3*1000, # in milliseconds
        n_intervals = 0,
        max_intervals = -1
    )
], fluid = True)


@callback(
    Output('interval-setup', 'max_intervals'),
    [Input('tabs', 'active_tab')]
)
def stop_intervals(active_tab):
    if active_tab == 'tab-1':
        return -1
    else:
        return 0
    

@callback(
    Output('interval-calibration', 'max_intervals'),
    [Input('tabs', 'active_tab'),
     Input("calib-run-button", "n_clicks"),
     Input("calib-stop-button", "n_clicks")]
)
def stop_intervals(active_tab, btn_run, btn_stop):
    if active_tab == 'tab-2' and btn_run == ctx.triggered_id:
        calibrationTest(50) # 10 samples, el valor hay que pillarlo del input
        return -1
    elif btn_stop == ctx.triggered_id or active_tab != 'tab-2':
        return 0


@callback(
    [Output("indicador-llenar", "style"),
     Output("indicador-vaciar", "style")],
    [Input("boton-llenar", "n_clicks"),
     Input("boton-vaciar", "n_clicks"),
     Input("boton-parar", "n_clicks")]
)
def update_indicators(btn_llenar, btn_vaciar, btn_parar):
    # iluminar el boton que se presionó
    style_on = {"height": "10px", "background-color": "green", "margin-bottom": "10px"}
    style_off = {"height": "10px", "background-color": "transparent", "margin-bottom": "10px"}

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


@callback(
    Output("tabla-medidas", "data"),
    [Input('interval-setup', 'n_intervals')]
)
def update_indicators(n_intervals):
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_units = executor.submit(SCPI_Arduino('UNITS?'))
        future_RC_value = executor.submit(RC_circuit_value)

        units = future_units.result()
        RC_value = future_RC_value.result()
        na = "NaN"
        print(units, RC_value)
        return [
            {"medida": "Peso de la Báscula (g)", "valor": units},
            {"medida": "Medida Circuito RC", "valor": RC_value},
            {"medida": "Peso según Circuito RC", "valor": na},
        ]



@callback(
    Output("calib-graph", "figure"),
    [Input('interval-calibration', 'n_intervals')]
)
def update_indicators(n_intervals):
    calibrationList = []  # Assuming calibrationList is defined somewhere in your code
    # Plot calibrationList data in graph
    x_values = [data[0] for data in calibrationList]
    y_values = [data[1] for data in calibrationList]
    fig = go.Figure(data=go.Scatter(x=x_values, y=y_values, mode='markers'))
    
    return fig
    

def calibrationTest(sample):
    SCPI_Arduino('TARGETWEIGHT' + str(0))
    if SCPI_Arduino('UNITS?') < str(0):
        SCPI_Arduino('TARE')
    while SCPI_Arduino('UNITS?') > str(0):
        SCPI_Arduino('DEC')
    SCPI_Arduino('STOP')

    maxWeight = SCPI_Arduino('MAXWEIGHT?')
    step = maxWeight / sample

    for i in range(sample):
        SCPI_Arduino('TARGETWEIGHT' + str(step * i))
        while SCPI_Arduino('UNITS?') < str(step * i):
            pass
        RCValue = RC_circuit_value()
        Weight = SCPI_Arduino('UNITS?')
        calibrationList.append([RCValue, Weight])

        

if __name__ == '__main__':
    app.run_server(debug=True, use_reloader=False)