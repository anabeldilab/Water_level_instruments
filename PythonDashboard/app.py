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
import numpy as np
from scipy.optimize import curve_fit, root_scalar
import time

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
        if optimized_rc_params is not None:
            RC_Weight = find_weight_for_rc(RC_value, *optimized_rc_params)
        else:
            RC_Weight = "NaN"

        print(units, RC_value)
        return [
            {"measure": "Peso de la Báscula (g)", "value": units},
            {"measure": "Medida Circuito RC", "value": RC_value},
            {"measure": "Peso según Circuito RC", "value": RC_Weight},
        ]


calibrationList = []
stop_calibration = False
calibration_complete = False
optimized_rc_params = None


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
    Output('update-complete-flag', 'children'),
    [Input('interval-calibration', 'n_intervals')],
    [State("calib-sample-size", "value")]
)
def complete_calibration(n_clicks, sample_size):
    if sample_size is None or not isinstance(sample_size, int):
        sample_size = 5

    if len(calibrationList) >= sample_size + 1:
        return "Complete"
    return "Incomplete"


@callback(
    Output("calib-graph", "figure"),
    [Input("interval-calibration", "n_intervals"),
    Input("calib-adjust-button", "n_clicks")],
    prevent_initial_call = True
)
def update_graph(n_intervals, n_clicks):
    global stop_calibration, optimized_rc_params
    figure = {'data': []}
    if (stop_calibration):
        optimized_rc_params = None
        return {'data': []}
    elif (n_clicks):
        initial_guesses = [1, 0.01, 1] 

        x = np.array([item[0] for item in calibrationList], dtype=float)
        y = np.array([item[1] for item in calibrationList], dtype=float)

        optimized_rc_params, pcov = curve_fit(exp_func, x, y, p0=initial_guesses)

        predicted_rc_values = exp_func(x, *optimized_rc_params)

        graph_data = [
            go.Scatter(x = x, y = y, mode = 'lines+markers', name = 'Mediciones'),
            go.Scatter(x = x, y = predicted_rc_values, mode = 'lines', name = 'Ajuste'),
        ]
        figure = {'data': graph_data}
    else:
        graph_data = [
            go.Scatter(x = [item[0] for item in calibrationList], y = [item[1] for item in calibrationList], mode = 'lines+markers')
        ]
        figure = {'data': graph_data}
    return figure


@callback(
    Output("calibration-modal", "is_open"),
    [Input("calib-run-button", "n_clicks"),
     Input("close-modal", "n_clicks"),
     Input('update-complete-flag', 'children')],
    [State("calibration-modal", "is_open")]
)
def toggle_modal(run_btn, close_modal, update_status, is_open):
    if update_status == "Complete" and is_open:
        return False
    elif "calib-run-button" == ctx.triggered_id and not is_open:
        return True
    elif "close-modal" == ctx.triggered_id and is_open:
        return False
    return is_open


@callback(
    Output('graph-units-table', 'data'),
    [Input('interval-calibration', 'n_intervals')]
)
def update_graph_units_table(n_intervals):
    global stop_calibration
    if (stop_calibration):
        return {'weight': [], 'rc-value': []}
    formatted_data = [{'weight': pair[0], 'rc-value': pair[1]} for pair in calibrationList]

    return formatted_data


def calibrationTest(sample_size, calibrationList):
    with ThreadPoolExecutor(max_workers = 2) as executor:
        global stop_calibration

        units_str = SCPI_Arduino('UNITS?')
        print("Units: " + str(units_str))

        try:
            units = float(units_str)
            if units < 0:
                SCPI_Arduino('TARE')
        except (TypeError, ValueError):
            print("No se pudo convertir 'units' a un número.")

        maxWeight = SCPI_Arduino('MAXWEIGHT?') or 500
        step = float(maxWeight) / sample_size
        step = round(step, 2)

        print("Calibrating with " + str(sample_size) + " samples")
        print("Step number: " + str(step))

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


# Definición de la función de ajuste exponencial
def exp_func(x, a, b, c):
    return a * np.exp(-b * x) + c


def find_weight_for_rc(y, a, b, c):
    func = lambda x: exp_func(x, a, b, c) - y
    try:
        return root_scalar(func, method='newton', x0=0).root
    except Exception as e:
        print("Error al encontrar el peso para el valor RC:", e)
        return None

if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)