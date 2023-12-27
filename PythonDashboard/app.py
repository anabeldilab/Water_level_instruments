import dash
import dash_bootstrap_components as dbc
from dash import callback, Output, Input, ctx, dcc, State
from tabs import setupTab
from tabs import calibrationRCTab
from tabs import controlTab
from concurrent.futures import ThreadPoolExecutor
from SCPI_Control import SCPI_Arduino
from redpitaya_instrument import RC_circuit_value
import plotly.graph_objects as go

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(setupTab.setup_tab(), label = "Setup", tab_id = 'tab-1'),
        dbc.Tab(calibrationRCTab.calibration_tab(), label = "Calibración RC", tab_id = 'tab-2'),
        dbc.Tab(controlTab.control_auto_tab(), label = "Control automático", tab_id = 'tab-3'),
    ], id = 'tabs', active_tab = 'tab-1'),
    dcc.Interval(
        id = 'interval-setup',
        interval = 3 * 1000, # in milliseconds
        n_intervals = 0,
        max_intervals = -1
    ),
    dcc.Interval(
        id = 'interval-calibration',
        interval = 3 * 1000, 
        n_intervals = 0,
        max_intervals = 0
    ),
], fluid = True)


@callback(
    [Output('interval-setup', 'max_intervals'),
     Output('interval-calibration', 'max_intervals')],
    [Input('tabs', 'active_tab')]
)
def stop_intervals(active_tab):
    print(active_tab)
    if active_tab == 'tab-1':
        return -1, 0
    elif active_tab == 'tab-2':
        return 0, -1
    else:
        return 0, 0


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

    if "boton-parar" == ctx.triggered_id:
        SCPI_Arduino('STOP')
        return style_off, style_off
    if "boton-llenar" == ctx.triggered_id:
        SCPI_Arduino('INC')
        return style_on, style_off
    elif "boton-vaciar" == ctx.triggered_id:
        SCPI_Arduino('DEC')
        return style_off, style_on

    return style_off, style_off


@callback(
    Output("current-units-indicator", "children"),
    [Input("boton-tarar", "n_clicks"),
     Input("boton-escalar", "n_clicks")]
)
def scale_control(btn_tarar, btn_escalar):
    if "boton-tarar" == ctx.triggered_id:
        SCPI_Arduino('TARE')
    elif "boton-escalar" == ctx.triggered_id:
        SCPI_Arduino('CHANGEUNITS')


@callback(
    Output("current-units-measures", "data"),
    [Input('interval-setup', 'n_intervals')]
)
def update_table(n_intervals):
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_units = executor.submit(SCPI_Arduino, 'UNITS?')
        future_RC_value = executor.submit(RC_circuit_value)

        units = future_units.result()
        RC_value = future_RC_value.result()
        na = "NaN"
        print(units, RC_value)
        return [
            {"measure": "Peso de la Báscula (g)", "value": units},
            {"measure": "Medida Circuito RC", "value": RC_value},
            {"measure": "Peso según Circuito RC", "value": na},
        ]


calibrationList = []
stop_calibration = False


@callback(
    Output("calib-sample-size", "value"),
    Input("calib-run-button", "n_clicks"),
    State("calib-sample-size", "value"),
    prevent_initial_call = True
)
def update_graph(n_clicks, sample_size):
    if sample_size is None or sample_size <= 0:
        sample_size = 5

    global calibrationList
    calibrationList = []
    calibrationTest(sample_size, calibrationList)

    return sample_size


@callback(
    Output("calib-graph", "figure"),
    Input("interval-calibration", "n_intervals"),
    prevent_initial_call = True
)
def update_graph(n_intervals):
    if (stop_calibration):
        return {'data': []}
    graph_data = [
        go.Scatter(x = [item[0] for item in calibrationList], y = [item[1] for item in calibrationList], mode = 'lines+markers')
    ]
    figure = {'data': graph_data}
    return figure


@callback(
    Output("calibration-modal", "is_open"),
    [Input("calib-run-button", "n_clicks"), 
     Input("close-modal", "n_clicks")],
    [State("calibration-modal", "is_open")],
)
def toggle_modal(run_btn, close_modal, is_open):
    global stop_calibration
    if run_btn or close_modal:
        stop_calibration = True if close_modal else False
        return not is_open
    return is_open


@callback(
    Output('graph-units-table', 'data'),
    [Input('interval-calibration', 'n_intervals')]
)
def update_graph_units_table(n_intervals):
    formatted_data = [{'weight': pair[0], 'rc-value': pair[1]} for pair in calibrationList]

    return formatted_data


def calibrationTest(sample_size, calibrationList):
    with ThreadPoolExecutor(max_workers = 2) as executor:
        global stop_calibration
        units = SCPI_Arduino('UNITS?')
        if isinstance(units, (int, float)) and units < 0:
            SCPI_Arduino('TARE')

        wait_for_water_level_to_reach(0)

        maxWeight = SCPI_Arduino('MAXWEIGHT?') or 500
        step = float(maxWeight) / sample_size


        print("Calibrating with " + str(sample_size) + " samples")

        for i in range(sample_size + 1):
            print("Target Weight: " + str(step * i))
            wait_for_water_level_to_reach(step * i)
            if stop_calibration:
                print("Calibration stopped by user")
                calibrationList.clear()
                break
            future_units = executor.submit(SCPI_Arduino, 'UNITS?')
            future_RC_value = executor.submit(RC_circuit_value)
            Weight = future_units.result()
            RCValue = future_RC_value.result()
            print("Weight: " + str(Weight) + " RCValue: " + str(RCValue))
            calibrationList.append([Weight, RCValue])


def wait_for_water_level_to_reach(target_level):
    print('TARGETWEIGHT ' + str(target_level))
    SCPI_Arduino('TARGETWEIGHT ' + str(target_level))
    waterLevelReached = SCPI_Arduino('WATERLEVELREACHED?')
    print("Water Level Reached: " + waterLevelReached)
    while waterLevelReached != '1':
        if stop_calibration:
            SCPI_Arduino('STOP')
            print("Calibration stopped water level not reached")
            break
        waterLevelReached = SCPI_Arduino('WATERLEVELREACHED?')
    print("Water Level Reached: " + waterLevelReached)


if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)