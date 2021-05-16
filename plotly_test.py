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
num_clicks = 1
refresh_rate = (1/10 * 1000)  # change the first number of the denominator to the refreshes you want per second
df = pd.read_csv(file)

class variables:
    most_recent_time = df['time'][len(df)-1]

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
    dcc.Tabs(id='tabs', value="qo_tab", children=[
        dcc.Tab(id='qo_tab', label='Quick Overview', value='qo_tab', children=[
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
        dcc.Tab(id="all_sensors_tab", label="All Sensors", value='all_sensors_tab'),
        dcc.Tab(id="high_sensors_tab", label='High Priority Sensors', value='high_sensors_tab'),
        dcc.Tab(id="medium_sensors_tab", label='Medium Priority Sensors', value='medium_sensors_tab'),
        dcc.Tab(id="low_sensors_tab", label='Low Priority Sensors', value='low_sensors_tab'),
        dcc.Tab(id="safety_sensors_tab", label='Safety Sensors', value='safety_sensors_tab'),
    ]),
    dcc.Interval(
        id='interval-component',
        interval= refresh_rate,  # in milliseconds
    )
])


# ____________________________________________________________
# Helper Functions


def create_header(sensor):
    return html.H3(sensor['label'])


def create_graph(sensor, data):
    return dcc.Graph(id=sensor['id'] + "_graph",
                     figure=go.Figure(go.Scatter(x=data['time'], y=data[sensor['id']])).update_layout(
                         title_text=sensor['label'] + " Graph",
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
    dash.dependencies.Output('container-button-basic', 'children'),
    dash.dependencies.Output('qo_tab', 'children'),
    dash.dependencies.Output('all_sensors_tab', 'children'),
    dash.dependencies.Output('high_sensors_tab', 'children'),
    dash.dependencies.Output('medium_sensors_tab', 'children'),
    dash.dependencies.Output('low_sensors_tab', 'children'),
    dash.dependencies.Output('safety_sensors_tab', 'children'),
    [dash.dependencies.Input('dropdown-gauge', 'value'),
     dash.dependencies.Input('dropdown-graph', 'value'),
     dash.dependencies.Input('interval-component', 'n_intervals'),
     dash.dependencies.Input('pause-button', 'n_clicks'),
     dash.dependencies.Input('tabs', 'value')]
)
def update_front_page(id_gauge, id_graph, n_intervals, n_clicks, active_tab):
    data = pd.read_csv(file)
    if data['time'][len(data)-1] == variables.most_recent_time:
        variables.most_recent_time = variables.most_recent_time
        # return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

        # remove this comment if you want the page to update ONLY when a
        # new piece of data is received, this can improve efficiency but if you switch tabs, it will take until the
        # next piece of data is received to load the tab
    else:
        variables.most_recent_time = data['time'][len(data)-1]

    if active_tab == 'qo_tab':
        return create_quick_overview_tab(id_gauge, id_graph, n_clicks, data)
    elif active_tab == 'all_sensors_tab':
        return create_all_sensors_tab(data, n_clicks)
    elif active_tab == 'high_sensors_tab':
        return create_high_sensors_tab(data, n_clicks)
    elif active_tab == 'medium_sensors_tab':
        return create_med_senors_tab(data, n_clicks)
    elif active_tab == 'low_sensors_tab':
        return create_low_sensors_tab(data, n_clicks)
    elif active_tab == 'safety_sensors_tab':
        return create_low_sensors_tab(data, n_clicks)
    else:
        raise PreventUpdate


def create_quick_overview_tab(id_gauge, id_graph, n_clicks, data):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        sensor_graph = find_sensor_given_id(id_graph)
        if sensor_graph:
            figure = go.Figure(go.Scatter(x=data['time'], y=data[sensor_graph['id']])).update_layout(
                title_text=sensor_graph['label'] + " Graph", xaxis=dict(rangeslider=dict(visible=True), type="linear"))
        else:
            figure = no_update
    else:
        button = 'The live graphs are currently paused.'
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

    return maxVal, minVal, units, label, value, figure, button, no_update, no_update, no_update, no_update, no_update, no_update


def create_all_sensors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
    else:
        button = 'The live graphs are currently paused.'
    all_children = create_grad_bars(data)
    return no_update, no_update, no_update, no_update, no_update, no_update, button, no_update, all_children, no_update, no_update, no_update, no_update


def create_high_sensors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        high_children = create_graphs(sensors.hp_sens, data)
    else:
        button = 'The live graphs are currently paused.'
        high_children = no_update
    return no_update, no_update, no_update, no_update, no_update, no_update, button, no_update, no_update, high_children, no_update, no_update, no_update


def create_med_senors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        medium_children = create_graphs(sensors.mp_sens, data)
    else:
        button = 'The live graphs are currently paused.'
        medium_children = no_update
    return no_update, no_update, no_update, no_update, no_update, no_update, button, no_update, no_update, no_update, medium_children, no_update, no_update


def create_low_sensors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        low_children = create_graphs(sensors.lp_sens, data)
    else:
        button = 'The live graphs are currently paused.'
        low_children = no_update
    return no_update, no_update, no_update, no_update, no_update, no_update, button, no_update, no_update, no_update, no_update, low_children, no_update


def create_safe_sensors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        safety_children = create_graphs(sensors.s_sens, data)
    else:
        button = 'The live graphs are currently paused.'
        safety_children = no_update
    return no_update, no_update, no_update, no_update, no_update, no_update, button, no_update, no_update, no_update, no_update, no_update, safety_children


if __name__ == '__main__':
    app.run_server(debug=True)
