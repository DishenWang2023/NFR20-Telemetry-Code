import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
import sensor_list as sensors
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#111111',
    'text': '#7FDBFF'
}

# change this file that the csv is stored in
file = 'TelemetryData/data.csv'

df = pd.read_csv(file)
num_clicks = 1


def create_options():
    result = []
    for sensor in sensors.hp_sens:
        result.append({'label': sensors.hp_sens[sensor]['label'],
                       'value': sensors.hp_sens[sensor]['id']})
    for sensor in sensors.mp_sens:
        result.append({'label': sensors.mp_sens[sensor]['label'],
                       'value': sensors.mp_sens[sensor]['id']})
    for sensor in sensors.lp_sens:
        result.append({'label': sensors.lp_sens[sensor]['label'],
                       'value': sensors.lp_sens[sensor]['id']})
    for sensor in sensors.s_sens:
        result.append({'label': sensors.s_sens[sensor]['label'],
                       'value': sensors.s_sens[sensor]['id']})
    return result


app.layout = html.Div([
    html.Div(
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H5("Northwestern Formula Racing"),
                    html.H6("Telemetry Data")])]),
    html.Button('Pause/Resume', id='pause-button', n_clicks=1),
    html.Div(id='container-button-basic'),
    dcc.Tabs([
        dcc.Tab(label='Quick Overview', children=[
            dcc.Dropdown(id='dropdown-graph',
                         options=create_options(),
                         value='fl_vss'),
            dcc.Graph(id='dropdown-graph_show'),
            dcc.Dropdown(id='dropdown-gauge',
                         options=create_options(),
                         value='fl_vss'),
            daq.Gauge(id='dropdown-gauge_show',
                      showCurrentValue=True)
        ]),
        dcc.Tab(id="all_sensors_tab", label="All Sensors"),
        dcc.Tab(id="high_sensors_tab", label='High Priority Sensors'),
        dcc.Tab(id="medium_sensors_tab", label='Medium Priority Sensors'),
        dcc.Tab(id="low_sensors_tab", label='Low Priority Sensors'),
        dcc.Tab(id="safety_sensors_tab", label='Safety Sensors'),
    ]),
    dcc.Interval(
        id='interval-component',
        interval=1 * 1000,  # in milliseconds
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
    dash.dependencies.Output('dropdown-gauge_show', 'max'),
    dash.dependencies.Output('dropdown-gauge_show', 'min'),
    dash.dependencies.Output('dropdown-gauge_show', 'units'),
    dash.dependencies.Output('dropdown-gauge_show', 'label'),
    dash.dependencies.Output('dropdown-gauge_show', 'value'),
    dash.dependencies.Output('dropdown-graph_show', 'figure'),
    [dash.dependencies.Input('dropdown-gauge', 'value'),
     dash.dependencies.Input('dropdown-graph', 'value'),
     dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_front_page(id_gauge, id_graph, n_intervals):
    if id_gauge in sensors.hp_sens:
        sensor_gauge = sensors.hp_sens[id_gauge]
    elif id_gauge in sensors.mp_sens:
        sensor_gauge = sensors.mp_sens[id_gauge]
    elif id_gauge in sensors.lp_sens:
        sensor_gauge = sensors.lp_sens[id_gauge]
    elif id_gauge in sensors.s_sens:
        sensor_gauge = sensors.s_sens[id_gauge]
    else:
        raise PreventUpdate

    if id_graph in sensors.hp_sens:
        sensor_graph = sensors.hp_sens[id_graph]
    elif id_graph in sensors.mp_sens:
        sensor_graph = sensors.mp_sens[id_graph]
    elif id_graph in sensors.lp_sens:
        sensor_graph = sensors.lp_sens[id_graph]
    elif id_graph in sensors.s_sens:
        sensor_graph = sensors.s_sens[id_graph]
    else:
        raise PreventUpdate

    data = pd.read_csv(file)
    maxVal = sensor_gauge['max_value']
    minVal = sensor_gauge['min_value']
    units = sensor_gauge['units']
    label = sensor_gauge['label']
    value = data[sensor_gauge['id']][len(data) - 1]
    figure = go.Figure(go.Scatter(x=data['time'], y=data[sensor_graph['id']])).update_layout(
                         xaxis=dict(rangeslider=dict(visible=True), type="linear"))
    return maxVal, minVal, units, label, value, figure


def create_grad_bar(sensor, data):
    maxVal = sensor['max_value']
    minVal = sensor['min_value']
    return daq.GraduatedBar(id=sensor['id'] + "_grad_bar",
                            color={"ranges": {"green": [minVal, maxVal * .8],
                                              "yellow": [maxVal * .8, maxVal * .9],
                                              "red": [maxVal * .9, maxVal]}},
                            showCurrentValue=True, size=1000, max=maxVal,
                            step=(abs(minVal) + abs(maxVal)) / 100,
                            value=abs(data[sensor['id']][len(data) - 1]))


@app.callback(
    dash.dependencies.Output('all_sensors_tab', 'children'),
    [dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_all_sensors_tab(n_intervals):
    data = pd.read_csv(file)
    result = []
    for sensor in sensors.hp_sens:
        result.append(create_header(sensors.hp_sens[sensor]))
        result.append(create_grad_bar(sensors.hp_sens[sensor], data))
    for sensor in sensors.mp_sens:
        result.append(create_header(sensors.mp_sens[sensor]))
        result.append(create_grad_bar(sensors.mp_sens[sensor], data))
    for sensor in sensors.lp_sens:
        result.append(create_header(sensors.lp_sens[sensor]))
        result.append(create_grad_bar(sensors.lp_sens[sensor], data))
    for sensor in sensors.s_sens:
        result.append(create_header(sensors.s_sens[sensor]))
        result.append(create_grad_bar(sensors.s_sens[sensor], data))
    return result


def create_header(sensor):
    result = sensor['label']
    return html.H3(result)


def create_graph(sensor, data):
    return dcc.Graph(id=sensor['id'] + "_graph",
                     figure=go.Figure(go.Scatter(x=data['time'], y=data[sensor['id']])).update_layout(
                         xaxis=dict(rangeslider=dict(visible=True), type="linear")))


def create_graphs(sensors_lst, data):
    result = []
    for sensor in sensors_lst:
        result.append(create_header(sensors_lst[sensor]))
        result.append(create_graph(sensors_lst[sensor], data))
    return result


@app.callback(
    dash.dependencies.Output('high_sensors_tab', 'children'),
    dash.dependencies.Output('medium_sensors_tab', 'children'),
    dash.dependencies.Output('low_sensors_tab', 'children'),
    dash.dependencies.Output('safety_sensors_tab', 'children'),
    [dash.dependencies.Input('pause-button', 'n_clicks'),
     dash.dependencies.Input('interval-component', 'n_intervals')]
)
def update_graphs(n_clicks, n_intervals):
    if n_clicks % 2 == 0:
        raise PreventUpdate
    data = pd.read_csv(file)
    high_children = create_graphs(sensors.hp_sens, data)
    medium_children = create_graphs(sensors.mp_sens, data)
    low_children = create_graphs(sensors.lp_sens, data)
    safety_children = create_graphs(sensors.s_sens, data)
    return high_children, medium_children, low_children, safety_children


if __name__ == '__main__':
    app.run_server(debug=True)
