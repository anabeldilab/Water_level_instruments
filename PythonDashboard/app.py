import dash
import dash_bootstrap_components as dbc
from tabs import setupTab
from tabs import calibrationRCTab
from tabs import controlTab

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(setupTab.setup_tab(), label="Setup"),
        dbc.Tab(calibrationRCTab.calibration_tab(), label="Calibración RC"),
        dbc.Tab(controlTab.control_auto_tab(), label="Control automático"),
    ]),
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)