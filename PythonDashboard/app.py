import dash
import dash_bootstrap_components as dbc
from tabs import setupTab

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.DARKLY])

app.layout = dbc.Container([
    dbc.Tabs([
        dbc.Tab(setupTab.setup_tab(), label="Setup"),
        # ... otras pestañas ...
    ]),
], fluid=True)

if __name__ == '__main__':
    app.run_server(debug=True)