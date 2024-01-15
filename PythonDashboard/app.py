import dash
import dash_bootstrap_components as dbc
from dash import callback, Output, Input, ctx, dcc, State
from tabs import setupTab
from tabs import calibrationRCTab
from tabs import controlTab
from concurrent.futures import ThreadPoolExecutor
from dash.exceptions import PreventUpdate
from arduino_scpi import arduino_SCPI
from redpitaya_instrument import RC_circuit_value, set_rc_circuit_frequency
import plotly.graph_objects as go
import numpy as np
from scipy.optimize import curve_fit, root_scalar
from datetime import datetime
from collections import deque
import time


app = dash.Dash(__name__, external_stylesheets = [dbc.themes.DARKLY])

calibrationList = []
weightData = []
weightData = deque(maxlen=20)
stop_calibration = False
calibration_complete = False
optimized_rc_params = None
adjustment = False
global_max_weight = None
global_units_aut_control = None
global_hysteresis = None
global_target_weight = None
global_capacitor_water_level_reached = True

app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(setupTab.setup_tab(), label = "Setup", tab_id = 'tab-1'),
        dbc.Tab(calibrationRCTab.calibration_tab(), label = "Calibración RC", tab_id = 'tab-2'),
        dbc.Tab(controlTab.control_auto_tab(), label = "Control automático", tab_id = 'tab-3'),
    ], id = 'tabs', active_tab = 'tab-1'),
    dcc.Store(id='last-tab', data=''),
    dcc.Interval(
        id = 'interval-setup',
        interval = 3 * 1000, # in milliseconds
        n_intervals = 0,
        max_intervals = -1
    ),
    dcc.Interval(
        id = 'interval-calibration',
        interval = 0.5 * 1000, 
        n_intervals = 0,
        max_intervals = 0
    ),
    dcc.Interval(
        id = 'interval-control',
        interval = 3 * 1000, 
        n_intervals = 0,
        max_intervals = 0
    ),
], fluid = True)


@callback(
    [Output('interval-setup', 'max_intervals'),
     Output('interval-calibration', 'max_intervals'),
     Output('interval-control', 'max_intervals')],
    [Input('tabs', 'active_tab')]
)
def stop_intervals(active_tab):
    print(active_tab)
    if active_tab == 'tab-1':
        return -1, 0, 0
    elif active_tab == 'tab-2':
        return 0, -1, 0
    elif active_tab == 'tab-3':
        return 0, 0, -1
    else:
        return 0, 0, 0


@callback(
    [Output("boton-llenar", "style"),
     Output("boton-vaciar", "style")],
    [Input("boton-llenar", "n_clicks"),
     Input("boton-vaciar", "n_clicks"),
     Input("boton-parar", "n_clicks")]
)
def update_indicators(btn_llenar, btn_vaciar, btn_parar):
    style_on_button = {"border": "5px solid green", "border-radius": "5px"}
    style_off_button = {"border": "5px solid transparent", "border-radius": "5px"}

    if "boton-parar" == ctx.triggered_id:
        arduino_SCPI('STOP')
        return style_off_button, style_off_button
    if "boton-llenar" == ctx.triggered_id:
        arduino_SCPI('INC')
        return style_on_button, style_off_button
    elif "boton-vaciar" == ctx.triggered_id:
        arduino_SCPI('DEC')
        return style_off_button, style_on_button

    return style_off_button, style_off_button


@callback(
    Output("current-units-indicator", "children"),
    Input("boton-tarar", "n_clicks")
)
def scale_control(btn_tarar):
    if "boton-tarar" == ctx.triggered_id:
        arduino_SCPI('TARE')


@callback(
    Output("modal-escalar", "is_open"),
    [Input("boton-escalar", "n_clicks"),
    Input("boton-guardar-escalado", "n_clicks")],
    [State("modal-escalar", "is_open")]
)
def toggle_calibrate_modal(btn_escalar, btn_save_scalar, is_open):
    if "boton-escalar" == ctx.triggered_id and not is_open:
        return True
    elif "boton-guardar-escalado" == ctx.triggered_id and is_open:
        return False
    return is_open


@callback(
    Output("input-max-peso", "value"),
    [Input("boton-max-peso", "n_clicks")],
    [State("input-max-peso", "value")],
)
def update_max_weight(n_clicks, max_weight):
    if n_clicks is None:
        raise dash.exceptions.PreventUpdate
    if max_weight is None:
        max_weight = 500
    arduino_SCPI('MAXWEIGHT ' + str(max_weight))
    return max_weight


@callback(
    Output('input-frecuencia', 'value'),
    Input('boton-send-freqrc', 'n_clicks'),
    State('input-frecuencia', 'value')
)
def update_frequency(n_clicks, freq):
    if n_clicks is None:
        raise PreventUpdate
    newFreq = freq or 2000
    set_rc_circuit_frequency(newFreq)
    return newFreq


@callback(
    Output("current-units-measures", "data"),
    [Input('interval-setup', 'n_intervals')],
    [State('tabs', 'active_tab')]
)
def update_table(n_intervals, active_tab):
    if active_tab != 'tab-1':
        raise PreventUpdate
    with ThreadPoolExecutor(max_workers=2) as executor:
        future_units = executor.submit(arduino_SCPI, 'UNITS?')
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


@callback(
    Output("calib-sample-size", "value"),
    Input("calib-run-button", "n_clicks"),
    State("calib-sample-size", "value"),
    prevent_initial_call = True
)
def update_graph(n_clicks, sample_size):
    if sample_size is None or sample_size <= 0:
        sample_size = 5

    global calibrationList, optimized_rc_params, adjustment
    calibrationList = []
    adjustment = False
    optimized_rc_params = None

    calibrationTest(sample_size, calibrationList)

    return sample_size


@callback(
    Output('update-complete-flag', 'children'),
    [Input('interval-calibration', 'n_intervals')],
    [State("calib-sample-size", "value"), 
     State("tabs", "active_tab")]
)
def complete_calibration(n_clicks, sample_size, active_tab):
    if active_tab != 'tab-2':
        raise PreventUpdate
    if sample_size is None or not isinstance(sample_size, int):
        sample_size = 5

    if len(calibrationList) >= sample_size + 1:
        return "Complete"
    return "Incomplete"


@callback(
    Output("calib-graph", "figure"),
    [Input("interval-calibration", "n_intervals"),
    Input("calib-adjust-button", "n_clicks")],
    State("tabs", "active_tab"),
    prevent_initial_call = True
)
def update_graph(n_intervals, n_clicks, active_tab):
    global adjustment
    if active_tab != 'tab-2':
        raise PreventUpdate

    global stop_calibration, optimized_rc_params
    layout = {
        'title': 'Circuito RC vs. Báscula',
        'xaxis': {'title': 'Peso Báscula (g)'},
        'yaxis': {'title': 'Medida Circuito RC'},
    }
    figure = {'data': [], 'layout': layout}

    if stop_calibration:
        optimized_rc_params = None
        adjustment = False
        return figure
    elif "calib-adjust-button" == ctx.triggered_id or adjustment:
        adjustment = True
        initial_guesses = [1, 0.01, 1] 

        x = np.array([item[0] for item in calibrationList], dtype=float)
        y = np.array([item[1] for item in calibrationList], dtype=float)

        optimized_rc_params, pcov = curve_fit(exp_func, x, y, p0=initial_guesses)

        predicted_rc_values = exp_func(x, *optimized_rc_params)

        graph_data = [
            go.Scatter(x=x, y=y, mode='lines+markers', name='Mediciones'),
            go.Scatter(x=x, y=predicted_rc_values, mode='lines', name='Ajuste'),
        ]
        figure = {'data': graph_data, 'layout': layout}
    else:
        graph_data = [
            go.Scatter(x=[item[0] for item in calibrationList], y=[item[1] for item in calibrationList], mode='lines+markers')
        ]
        figure = {'data': graph_data, 'layout': layout}

    return figure


@callback(
    Output("calibration-modal", "is_open"),
    [Input("calib-run-button", "n_clicks"),
     Input("close-calib-modal", "n_clicks"),
     Input('update-complete-flag', 'children')],
    [State("calibration-modal", "is_open")]
)
def toggle_modal(run_btn, close_modal, update_status, is_open):
    global stop_calibration
    if update_status == "Complete" and is_open:
        return False
    elif "calib-run-button" == ctx.triggered_id and not is_open:
        stop_calibration = False
        return True
    elif "close-calib-modal" == ctx.triggered_id and is_open:
        stop_calibration = True
        return False
    return is_open


@callback(
    Output('calib-graph-units-table', 'data'),
    [Input('interval-calibration', 'n_intervals')],
    [State("tabs", "active_tab")]
)
def update_graph_units_table(n_intervals, active_tab):
    if active_tab != 'tab-2':
        raise PreventUpdate
    global stop_calibration
    if (stop_calibration):
        return [{'weight': None, 'rc-value': None}]
    formatted_data = [{'weight': pair[0], 'rc-value': pair[1]} for pair in calibrationList]

    return formatted_data


@callback(
    Output('my-tank-1', 'value'),
    [Input('interval-control', 'n_intervals')],
    [State("tabs", "active_tab"),
     State('sensor-dropdown', 'value')]
)
def update_tank(n_intervals, active_tab, value):
    with ThreadPoolExecutor(max_workers=1) as executor:
        global global_units_aut_control, global_max_weight, optimized_rc_params
        if active_tab != 'tab-3':
            raise PreventUpdate
        if value == 'bascula':
            future_global_units_aut_control = executor.submit(arduino_SCPI, 'UNITS?')
            global_units_aut_control = future_global_units_aut_control.result()
            try:
                global_units_aut_control = float(global_units_aut_control)
            except (TypeError, ValueError):
                print("No se pudo convertir 'units' a un número.")
                global_units_aut_control = None


        if (global_units_aut_control is None or global_max_weight is None):
            return 0
        print("Water Level: " + str(global_units_aut_control) + " Max Weight: " + str(global_max_weight))
        return float(global_units_aut_control) / float(global_max_weight) * 100
    

@callback(
    Output('control-graph', 'figure'),
    [Input('interval-control', 'n_intervals')],
    [State("tabs", "active_tab")]
)
def update_graph_units_table(n_intervals, active_tab):
    if active_tab != 'tab-3':
        raise PreventUpdate
    
    current_time = datetime.now().strftime("%H:%M:%S")
    weight = global_units_aut_control
    weightData.append([current_time, weight])
    new_data = [
        go.Scatter(
            x=[item[0] for item in weightData], 
            y=[item[1] for item in weightData], 
            mode='lines+markers',
            line_shape='spline',
        )
    ]

    return {
        'data': new_data,
        'layout': {
            'xaxis': {'title': 'Tiempo (s)', 'type': 'category'},
            'yaxis': {'title': 'Peso'}
        }
    }



@callback(
    [Output("consigna-input", "value"),
    Output("parametros-controlador", "value")],
    [Input("control-run-button", "n_clicks"),
     Input("control-stop-button", "n_clicks")],
    [State("consigna-input", "value"),
    State("parametros-controlador", "value"),
    State("sensor-dropdown", "value")],
    prevent_initial_call = True
)
def run_automatic_control(run_btn, stop_btn, target, hysteresis, value):
    global global_hysteresis, global_target_weight, global_capacitor_water_level_reached
    if "control-run-button" == ctx.triggered_id:
        if target is None or target <= 0:
            target = 100
        if hysteresis is None or hysteresis <= 0:
            hysteresis = 5
        global_hysteresis = hysteresis
        global_target_weight = target
        if value == 'bascula':
            arduino_SCPI('TOLERANCE ' + str(hysteresis))
            arduino_SCPI('TARGETWEIGHT ' + str(target))
        elif value == 'condensador':
            global_capacitor_water_level_reached = False
            with ThreadPoolExecutor(max_workers=1) as executor:
                if optimized_rc_params is not None:
                    global_hysteresis = float(global_hysteresis)
                    global_target_weight = float(global_target_weight)
                    print("Water level reached: " + str(global_capacitor_water_level_reached))
                    while not global_capacitor_water_level_reached:
                        global_capacitor_water_level_reached = controlWaterLevel()
        return target, hysteresis
    elif "control-stop-button" == ctx.triggered_id:
        global_capacitor_water_level_reached = True
        arduino_SCPI('STOP')
        return target, hysteresis
    

@callback(
    [Output('current_setpoint', 'children'),
    Output('current_weight', 'children'),
    Output('current_error', 'children')],
    [Input('interval-control', 'n_intervals'),
    Input("control-run-button", "n_clicks"),
    Input("control-stop-button", "n_clicks")],
    [State("tabs", "active_tab"),
    State("consigna-input", "value")]
)
def update_current_setpoint(n_intervals, btn_run, btn_stop, active_tab, consigna_value):
    global global_units_aut_control
    if active_tab != 'tab-3':
        raise PreventUpdate
    error = "-"
    if (consigna_value is None): 
        consigna_value = "-"
    if (global_units_aut_control is None):
        global_units_aut_control = "-"
    if isinstance(consigna_value, (int, float)):
        error = round(consigna_value - global_units_aut_control, 2)

    
    return f"{consigna_value}", f"{global_units_aut_control}", f"{error}"


@callback(
    Output('last-tab', 'data'),
    Input('tabs', 'active_tab'),
    State('last-tab', 'data')
)
def get_max_weight(active_tab, last_tab):
    global global_max_weight 
    if active_tab == 'tab-3' and active_tab != last_tab:
        global_max_weight = arduino_SCPI('MAXWEIGHT?')
        print("Max Weight: " + str(global_max_weight))
        time.sleep(1)
    return active_tab


def calibrationTest(sample_size, calibrationList):
    with ThreadPoolExecutor(max_workers = 2) as executor:
        global stop_calibration

        units_str = arduino_SCPI('UNITS?')
        print("Units: " + str(units_str))

        try:
            units = float(units_str)
            if units < 0:
                arduino_SCPI('TARE')
        except (TypeError, ValueError):
            print("No se pudo convertir 'units' a un número.")

        maxWeight = arduino_SCPI('MAXWEIGHT?') or 500
        step = float(maxWeight) / sample_size
        step = round(step, 2)

        print("Calibrating with " + str(sample_size) + " samples")
        print("Step number: " + str(step))

        for i in range(sample_size + 1):
            targetWeight = round(step * i, 2)
            print("Target Weight: " + str(targetWeight))
            wait_for_water_level_to_reach(targetWeight)
            if stop_calibration:
                print("Calibration stopped by user")
                calibrationList.clear()
                break
            future_units = executor.submit(arduino_SCPI, 'UNITS?')
            future_RC_value = executor.submit(RC_circuit_value)
            Weight = future_units.result()
            RCValue = future_RC_value.result()
            print("Weight: " + str(Weight) + " RCValue: " + str(RCValue))
            calibrationList.append([Weight, RCValue])


def wait_for_water_level_to_reach(target_level):
    print('TARGETWEIGHT ' + str(target_level))
    arduino_SCPI('TARGETWEIGHT ' + str(target_level))
    waterLevelReached = arduino_SCPI('WATERLEVELREACHED?')
    print("Water Level Reached: " + waterLevelReached)
    while waterLevelReached != '1':
        if stop_calibration:
            arduino_SCPI('STOP')
            print("Calibration stopped water level not reached")
            break
        waterLevelReached = arduino_SCPI('WATERLEVELREACHED?')
    print("Water Level Reached: " + waterLevelReached)


def isWeightReached(capacitorWeight):
    global global_hysteresis, global_target_weight
    return capacitorWeight >= global_target_weight - global_hysteresis and capacitorWeight <= global_target_weight + global_hysteresis


def waterLevelReached():
    arduino_SCPI("STOP")


def fillContainer():
    arduino_SCPI("INC")


def emptyContainer():
    arduino_SCPI("DEC")


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
    

def controlWaterLevel():
    global global_max_weight, global_target_weight, optimized_rc_params, global_units_aut_control
    capacitorValue = RC_circuit_value()
    global_units_aut_control = find_weight_for_rc(capacitorValue, *optimized_rc_params)
    capacitorWaterLevelReached = False
    
    if (global_units_aut_control is None or global_max_weight is None):
        print("Error al encontrar el peso para el valor RC")
        return capacitorWaterLevelReached
    global_max_weight = float(global_max_weight)
    if (isWeightReached(global_units_aut_control) or global_units_aut_control >= global_max_weight):
        waterLevelReached()
        capacitorWaterLevelReached = True
    elif (global_units_aut_control < global_target_weight):
        fillContainer()
    elif (global_units_aut_control > global_target_weight): 
        emptyContainer()
    return capacitorWaterLevelReached


if __name__ == '__main__':
    app.run_server(debug = True, use_reloader = False)