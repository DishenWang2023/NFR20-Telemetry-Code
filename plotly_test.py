import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_daq as daq
import pandas as pd
import plotly.graph_objs as go
import sensor_list_test as sensors
from dash.dash import no_update
from dash.exceptions import PreventUpdate

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

colors = {
    'background': '#4E2A84',
    'text': '#FFFFFF'
}

# change this file that the csv is stored in
file = 'TelemetryData/data.csv'
df = pd.read_csv(file)
num_clicks = 1


def all_sensors():
    result = []
    for sensor in sensors.hp_sens:
        result.append(sensors.hp_sens[sensor])
    for sensor in sensors.mp_sens:
        result.append(sensors.mp_sens[sensor])
    for sensor in sensors.lp_sens:
        result.append(sensors.lp_sens[sensor])
    for sensor in sensors.s_sens:
        result.append(sensors.s_sens[sensor])
    return result


all_sensors_lst = all_sensors()


def create_options():
    result = []
    for i in range(len(all_sensors_lst)):
        result.append({'label': all_sensors_lst[i]['label'],
                       'value': all_sensors_lst[i]['id']})
    return result


app.layout = html.Div([
    html.Div(
        style={'backgroundColor': colors['background']},
        id="banner",
        className="banner",
        children=[
            html.Div(
                id="banner-text",
                children=[
                    html.H4(children="Northwestern Formula Racing",
                            style={'color': colors['text'],
                                   'textAlign': 'center',
                                   'font-family': 'campton'}),
                    html.H6(children="Telemetry Data",
                            style={'color': colors['text'],
                                   'textAlign': 'center',
                                   'font-family': 'campton'})]
            )]),
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


# ____________________________________________________________
# Helper Functions


def create_header(sensor):
    return html.H3(sensor['label'])


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


def create_grad_bars(data):
    result = []
    for i in range(len(all_sensors_lst)):
        result.append(create_header(all_sensors_lst[i]))
        result.append(create_grad_bar(all_sensors_lst[i], data))
    return result


def find_sensor_given_id(id):
    if id in sensors.hp_sens:
        return sensors.hp_sens[id]
    elif id in sensors.mp_sens:
        return sensors.mp_sens[id]
    elif id in sensors.lp_sens:
        return sensors.lp_sens[id]
    elif id in sensors.s_sens:
        return sensors.s_sens[id]
    else:
        return False


# ____________________________________________________________
# Callbacks


# ____________________________________________________________
# Dropdown graph and gauge
@app.callback(
    dash.dependencies.Output('dropdown-gauge_show', 'max'),
    dash.dependencies.Output('dropdown-gauge_show', 'min'),
    dash.dependencies.Output('dropdown-gauge_show', 'units'),
    dash.dependencies.Output('dropdown-gauge_show', 'label'),
    dash.dependencies.Output('dropdown-gauge_show', 'value'),
    dash.dependencies.Output('dropdown-graph_show', 'figure'),
    dash.dependencies.Output('all_sensors_tab', 'children'),
    dash.dependencies.Output('container-button-basic', 'children'),
    dash.dependencies.Output('high_sensors_tab', 'children'),
    dash.dependencies.Output('medium_sensors_tab', 'children'),
    dash.dependencies.Output('low_sensors_tab', 'children'),
    dash.dependencies.Output('safety_sensors_tab', 'children'),
    [dash.dependencies.Input('dropdown-gauge', 'value'),
     dash.dependencies.Input('dropdown-graph', 'value'),
     dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks')]
)
def update_front_page(id_gauge, id_graph, n_intervals, n_clicks):
    data = pd.read_csv(file)
    if n_clicks % 2 == 1:
        clicks = 'The live graphs are currently being updated.'
        high_children = create_graphs(sensors.hp_sens, data)
        medium_children = create_graphs(sensors.mp_sens, data)
        low_children = create_graphs(sensors.lp_sens, data)
        safety_children = create_graphs(sensors.s_sens, data)
        sensor_graph = find_sensor_given_id(id_graph)
        if sensor_graph:
            figure = go.Figure(go.Scatter(x=data['time'], y=data[sensor_graph['id']])).update_layout(
                xaxis=dict(rangeslider=dict(visible=True), type="linear"))
        else:
            figure = no_update
    else:
        clicks = 'The live graphs are currently paused.'
        high_children = no_update
        medium_children = no_update
        low_children = no_update
        safety_children = no_update
        figure = no_update

    sensor_gauge = find_sensor_given_id(id_gauge)
    if sensor_gauge:
        maxVal = sensor_gauge['max_value']
        minVal = sensor_gauge['min_value']
        units = sensor_gauge['units']
        label = sensor_gauge['label']
        value = data[sensor_gauge['id']][len(data) - 1]
    else:
        maxVal = no_update
        minVal = no_update
        units = no_update
        label = no_update
        value = no_update

    # Updates the gauge and the graph on the quick overview tab

    # Updates the children for the all sensors tab
    children = create_grad_bars(data)

    return maxVal, minVal, units, label, value, figure, children, clicks, high_children, medium_children, low_children, safety_children


if __name__ == '__main__':
    app.run_server(debug=True)
