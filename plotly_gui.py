import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate
from dash.dependencies import Input, Output
import plotly.express as px
from sensor_list import used_sensors_list as used_sensors

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

df = pd.read_csv('data.csv')
params = list(df)
num_clicks = 1

app.layout = html.Div([
    html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Northwestern Formula Racing"),
                    html.H6("Telemetry Data"),
                ],
            ),
        ],
    ),
    html.Button(
        'Pause/Resume',
        id='pause-button',
        n_clicks=1
    ),
    html.Div(id='container-button-basic',
             children='Enter a value and press submit'),
    dcc.Tabs([
        dcc.Tab(label='Quick Overview', children=[
            html.H3("Vehicle Speed"),
            daq.Gauge(id='rpm-gauge',
                      max=200,
                      min=0,
                      value=100,
                      ),
            html.H3("Throttle Position"),
            daq.GraduatedBar(id='tps-grad-bar',
                             showCurrentValue=True,
                             size=1000,
                             max=100,
                             value=50
                             )
        ]),
        dcc.Tab(label='High Priority Sensors', children=[
            html.H3("Front Left Wheel Speed"),
            daq.LEDDisplay(id='fl_vss_LED',
                           label='Front Left Wheel Speed',
                           ),
            dcc.Graph(id='fl_vss_graph'),
            html.H3("Front Right Wheel Speed"),
            daq.LEDDisplay(id='fr_vss_LED',
                           label='Front Right Wheel Speed',
                           ),
            dcc.Graph(id='fr_vss_graph'),
            html.H3("Back Left Wheel Speed"),
            dcc.Graph(id='bl_vss_graph'),
            html.H3("Back Right Wheel Speed"),
            dcc.Graph(id='br_vss_graph'),
        ]),
        dcc.Tab(label='Medium Priority Sensors', children=[
            html.H3("Front Left Suspension Potentiometer"),
            dcc.Graph(id='fl_sus_pot_graph'),
            html.H3("Front Right Suspension Potentiometer"),
            dcc.Graph(id='fr_sus_pot_graph'),
            html.H3("Back Left Suspension Potentiometer"),
            dcc.Graph(id='bl_sus_pot_graph'),
            html.H3("Back Right Suspension Potentiometer"),
            dcc.Graph(id='br_sus_pot_graph'),
            html.H3("Steering Angle"),
            dcc.Graph(id='steer_ang_graph'),
        ]),
        dcc.Tab(label='Low Priority Sensors', children=[
            html.H3("Throttle Position"),
            dcc.Graph(id='tps_graph'),
            html.H3("Oil Pressure"),
            dcc.Graph(id='oil_pres_graph'),
            html.H3("Oil Temperature"),
            dcc.Graph(id='oil_temp_graph'),
            html.H3("Intake Manifold Air Pressure"),
            dcc.Graph(id='map_graph'),
            html.H3("Intake Manifold Air Temperature"),
            dcc.Graph(id='mat_graph'),
        ]),
        dcc.Tab(label='Safety Sensors', children=[
            html.H3("Front Left Brake Temperature"),
            dcc.Graph(id='fl_brk_tmp_graph'),
            html.H3("Front Right Brake Temperature"),
            dcc.Graph(id='fr_brk_tmp_graph'),
            html.H3("Back Left Brake Temperature"),
            dcc.Graph(id='bl_brk_tmp_graph'),
            html.H3("Back Right Brake Temperature"),
            dcc.Graph(id='br_brk_tmp_graph'),
            html.H3("Front Brake Pressure"),
            dcc.Graph(id='f_brk_pres_graph'),
            html.H3("Back Brake Pressure"),
            dcc.Graph(id='b_brk_pres_graph'),
            html.H3("Coolant Temperature"),
            dcc.Graph(id='cool_temp_graph'),
        ]),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
        n_intervals=0
    )
])


# Updating the button

@app.callback(
    dash.dependencies.Output('container-button-basic', 'children'),
    [dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_button(n_clicks):
    if n_clicks % 2 == 1:
        return 'The live graphs are currently being updated.'
    elif n_clicks % 2 == 0:
        return 'The live graphs are currently paused.'
    else:
        return 'There is a problem.'


# Updating the FL_VSS components

@app.callback(
    dash.dependencies.Output('fl_vss_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_fl_vss_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fl_vss']))
    fig.update_layout(title_text="Front Left Wheel Speed Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig

# Updating FR_VSS Components

@app.callback(
    dash.dependencies.Output('fr_vss_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_fr_vss_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fr_vss']))
    fig.update_layout(title_text="Front Right Wheel Speed Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating BL_VSS Components

@app.callback(
    dash.dependencies.Output('bl_vss_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['bl_vss']))
    fig.update_layout(title_text="Back Left Wheel Speed Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating BR_VSS Components

@app.callback(
    dash.dependencies.Output('br_vss_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['br_vss']))
    fig.update_layout(title_text="Back Right Wheel Speed Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating FL_SUS_POT Components

@app.callback(
    dash.dependencies.Output('fl_sus_pot_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fl_sus_pot']))
    fig.update_layout(title_text="Front Left Suspension Potentiometer Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating FR_SUS_POT Components

@app.callback(
    dash.dependencies.Output('fr_sus_pot_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fr_sus_pot']))
    fig.update_layout(title_text="Front Right Suspension Potentiometer Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating BL_SUS_POT Components

@app.callback(
    dash.dependencies.Output('bl_sus_pot_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['bl_sus_pot']))
    fig.update_layout(title_text="Back Left Suspension Potentiometer Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating BR_SUS_POT Components

@app.callback(
    dash.dependencies.Output('br_sus_pot_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['br_sus_pot']))
    fig.update_layout(title_text="Back Right Suspension Potentiometer Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating STEER_ANG Components

@app.callback(
    dash.dependencies.Output('steer_ang_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['steer_ang']))
    fig.update_layout(title_text="Steering Angle Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating TPS Components

@app.callback(
    dash.dependencies.Output('tps_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['tps']))
    fig.update_layout(title_text="Throttle Position Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating OIL_PRES Components

@app.callback(
    dash.dependencies.Output('oil_pres_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['oil_pres']))
    fig.update_layout(title_text="Oil Pressure Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating MAP Components

@app.callback(
    dash.dependencies.Output('map_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['map']))
    fig.update_layout(title_text="Intake Manifold Air Pressure Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating MAT Components

@app.callback(
    dash.dependencies.Output('mat_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['mat']))
    fig.update_layout(title_text="Intake Manifold Air Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating FL_BRK_TMP Components

@app.callback(
    dash.dependencies.Output('fl_brk_tmp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fl_brk_tmp']))
    fig.update_layout(title_text="Front Left Brake Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating FR_BRK_TMP Components

@app.callback(
    dash.dependencies.Output('fr_brk_tmp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fr_brk_tmp']))
    fig.update_layout(title_text="Front Right Brake Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating BL_BRK_TMP Components

@app.callback(
    dash.dependencies.Output('bl_brk_tmp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['bl_brk_tmp']))
    fig.update_layout(title_text="Back Left Brake Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating BR_BRK_TMP Components

@app.callback(
    dash.dependencies.Output('br_brk_tmp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['br_brk_tmp']))
    fig.update_layout(title_text="Back Right Brake Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating F_BRK_PRES Components

@app.callback(
    dash.dependencies.Output('f_brk_pres_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['f_brk_pres']))
    fig.update_layout(title_text="Front Brake Pressure Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating B_BRK_PRES Components

@app.callback(
    dash.dependencies.Output('b_brk_pres_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['b_brk_pres']))
    fig.update_layout(title_text="Back Brake Pressure Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


# Updating COOL_TEMP Components

@app.callback(
    dash.dependencies.Output('cool_temp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv('data.csv')
    fig = go.Figure(go.Scatter(x=data['time'], y=data['cool_temp']))
    fig.update_layout(title_text="Coolant Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig


if __name__ == '__main__':
    app.run_server(debug=False)
