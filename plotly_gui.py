import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# change this file that the csv is stored in
file = 'data.csv'

df = pd.read_csv(file)
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
            daq.Gauge(id='vs-gauge',
                      max=200,
                      min=0,
                      ),
            html.H3("Throttle Position"),
            daq.GraduatedBar(id='tps-grad-bar',
                             color={"gradient": True,
                                    "ranges": {"green": [0, 80], "yellow": [80, 90], "red": [90, 100]}},
                             showCurrentValue=True,
                             size=1000,
                             max=100,
                             )
        ]),
        dcc.Tab(label="All Sensors", children=[
            html.H4("Front Left Wheel Speed"),
            daq.GraduatedBar(id='fl_vss_grad_bar',
                             color={"gradient": True,
                                    "ranges": {"green": [0, 80], "yellow": [80, 90], "red": [90, 100]}},
                             showCurrentValue=True,
                             size=1000,
                             max=100,
                             ),
            html.H4("Front Right Wheel Speed"),
            daq.GraduatedBar(id='fr_vss_grad_bar',
                             color={"gradient": True,
                                    "ranges": {"green": [0, 80], "yellow": [80, 90], "red": [90, 100]}},
                             showCurrentValue=True,
                             size=1000,
                             max=100,
                             ),
            html.H4("Back Left Wheel Speed"),
            daq.GraduatedBar(id='bl_vss_grad_bar',
                             color={"gradient": True,
                                    "ranges": {"green": [0, 80], "yellow": [80, 90], "red": [90, 100]}},
                             showCurrentValue=True,
                             size=1000,
                             max=100,
                             ),
            html.H4("Back Right Wheel Speed"),
            daq.GraduatedBar(id='br_vss_grad_bar',
                             color={"gradient": True,
                                    "ranges": {"green": [0, 80], "yellow": [80, 90], "red": [90, 100]}},
                             showCurrentValue=True,
                             size=1000,
                             max=100,
                             ),
            ]),
        dcc.Tab(label='High Priority Sensors', children=[
            html.H3("Front Left Wheel Speed"),
            dcc.Graph(id='fl_vss_graph'),
            html.H3("Front Right Wheel Speed"),
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
    dash.dependencies.Output('vs-gauge', 'value'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_vs_gauge(n_intervals):
    data = pd.read_csv('data.csv')
    fr = data['fr_vss']
    fl = data['fl_vss']
    br = data['br_vss']
    bl = data['bl_vss']
    return (fr[len(fr) - 1] + fl[len(fl) - 1] + br[len(br) - 1] + bl[len(bl) - 1]) / 4



@app.callback(
    dash.dependencies.Output('tps-grad-bar', 'value'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_tps_grad_bar(n_intervals):
    data = pd.read_csv('data.csv')
    tps = data['TPS']
    return tps[len(tps) - 1]


# <editor-fold desc="Updating Graphs">
# <editor-fold desc="FL_VSS_GRAPH">
@app.callback(
    dash.dependencies.Output('fl_vss_graph', 'figure'),
    dash.dependencies.Output('fl_vss_grad_bar', 'value'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_fl_vss_graph(n_intervals, n_clicks):
    data = pd.read_csv(file)
    value = data['fl_vss']
    value = abs(value[len(value)-1])
    if n_clicks % 2 == 0:
        raise PreventUpdate
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fl_vss']))
    fig.update_layout(title_text="Front Left Wheel Speed Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig,value

# </editor-fold>

# <editor-fold desc="FR_VSS_GRAPH">
@app.callback(
    dash.dependencies.Output('fr_vss_graph', 'figure'),
    dash.dependencies.Output('fr_vss_grad_bar', 'value'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_fr_vss_graph(n_intervals, n_clicks):
    data = pd.read_csv(file)
    value = data['fr_vss']
    value = abs(value[len(value) - 1])
    if n_clicks % 2 == 0:
        raise PreventUpdate
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fr_vss']))
    fig.update_layout(title_text="Front Right Wheel Speed Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig, value
# </editor-fold>

# <editor-fold desc="BL_VSS_GRAPH">
@app.callback(
    dash.dependencies.Output('bl_vss_graph', 'figure'),
    dash.dependencies.Output('bl_vss_grad_bar', 'value'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    data = pd.read_csv(file)
    value = data['bl_vss']
    value = abs(value[len(value) - 1])
    if n_clicks % 2 == 0:
        raise PreventUpdate
    fig = go.Figure(go.Scatter(x=data['time'], y=data['bl_vss']))
    fig.update_layout(title_text="Back Left Wheel Speed Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig, value
# </editor-fold>

# <editor-fold desc="BR_VSS_GRAPH">
@app.callback(
    dash.dependencies.Output('br_vss_graph', 'figure'),
    dash.dependencies.Output('br_vss_grad_bar', 'value'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    data = pd.read_csv(file)
    value = data['br_vss']
    value = abs(value[len(value) - 1])
    if n_clicks % 2 == 0:
        raise PreventUpdate
    fig = go.Figure(go.Scatter(x=data['time'], y=data['br_vss']))
    fig.update_layout(title_text="Back Right Wheel Speed Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig, value
# </editor-fold>

# <editor-fold desc="FL_SUS_POT_GRAPH">
@app.callback(
    dash.dependencies.Output('fl_sus_pot_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fl_sus_pot']))
    fig.update_layout(title_text="Front Left Suspension Potentiometer Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="FR_SUS_POT_GRAPH">
@app.callback(
    dash.dependencies.Output('fr_sus_pot_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fr_sus_pot']))
    fig.update_layout(title_text="Front Right Suspension Potentiometer Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="BL_SUS_POT_GRAPH">
@app.callback(
    dash.dependencies.Output('bl_sus_pot_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['bl_sus_pot']))
    fig.update_layout(title_text="Back Left Suspension Potentiometer Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="BR_SUS_POT_GRAPH">
@app.callback(
    dash.dependencies.Output('br_sus_pot_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['br_sus_pot']))
    fig.update_layout(title_text="Back Right Suspension Potentiometer Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="STEER_ANG_GRAPH">
@app.callback(
    dash.dependencies.Output('steer_ang_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['steer_ang']))
    fig.update_layout(title_text="Steering Angle Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="TPS_GRAPH">
# Updating TPS Components

@app.callback(
    dash.dependencies.Output('tps_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['tps']))
    fig.update_layout(title_text="Throttle Position Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="OIL_PRES_GRAPH">
# Updating OIL_PRES Components

@app.callback(
    dash.dependencies.Output('oil_pres_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['oil_pres']))
    fig.update_layout(title_text="Oil Pressure Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="MAP_GRAPH">
# Updating MAP Components

@app.callback(
    dash.dependencies.Output('map_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['map']))
    fig.update_layout(title_text="Intake Manifold Air Pressure Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="MAT_GRAPH">
# Updating MAT Components

@app.callback(
    dash.dependencies.Output('mat_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['mat']))
    fig.update_layout(title_text="Intake Manifold Air Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="FL_BRK_TMP_GRAPH">
# Updating FL_BRK_TMP Components

@app.callback(
    dash.dependencies.Output('fl_brk_tmp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fl_brk_tmp']))
    fig.update_layout(title_text="Front Left Brake Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="FR_BRK_TMP_GRAPH">
# Updating FR_BRK_TMP Components

@app.callback(
    dash.dependencies.Output('fr_brk_tmp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['fr_brk_tmp']))
    fig.update_layout(title_text="Front Right Brake Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="BL_BRK_TMP_GRAPH">
# Updating BL_BRK_TMP Components

@app.callback(
    dash.dependencies.Output('bl_brk_tmp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['bl_brk_tmp']))
    fig.update_layout(title_text="Back Left Brake Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="BR_BRK_TMP_GRAPH">
# Updating BR_BRK_TMP Components

@app.callback(
    dash.dependencies.Output('br_brk_tmp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['br_brk_tmp']))
    fig.update_layout(title_text="Back Right Brake Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="F_BRK_PRES_GRAPH">
# Updating F_BRK_PRES Components

@app.callback(
    dash.dependencies.Output('f_brk_pres_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['f_brk_pres']))
    fig.update_layout(title_text="Front Brake Pressure Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="B_BRK_PRES_GRAPH">
# Updating B_BRK_PRES Components

@app.callback(
    dash.dependencies.Output('b_brk_pres_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['b_brk_pres']))
    fig.update_layout(title_text="Back Brake Pressure Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>

# <editor-fold desc="COOL_TEMP_GRAPH">
# Updating COOL_TEMP Components

@app.callback(
    dash.dependencies.Output('cool_temp_graph', 'figure'),
    [dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_graph(n_intervals, n_clicks):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    fig = go.Figure(go.Scatter(x=data['time'], y=data['cool_temp']))
    fig.update_layout(title_text="Coolant Temperature Graph")
    fig.update_layout(xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return fig
# </editor-fold>
# </editor-fold>


if __name__ == '__main__':
    app.run_server(debug=False)
