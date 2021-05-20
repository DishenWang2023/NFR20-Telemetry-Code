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
app = dash.Dash(__name__, external_stylesheets=external_stylesheets,update_title=None)
app.title = 'NFR Telemetry'

colors = {
    'background': '#4E2A84',
    'text': '#FFFFFF'
}

# change this file that the csv is stored in
file = 'TelemetryData/data.csv'
num_clicks = 1
refresh_rate = (1/5 * 1000)  # change the first number of the denominator to the refreshes you want per second
df = pd.read_csv(file)

class variables:
    most_recent_time = df['Time'][len(df)-1]

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
            html.H4(children="Sensor Graphs"),
            dcc.Dropdown(id='dropdown-graph',
                         options=create_options(),
                         value=['FL_VSS'],
                         multi=True),
            html.Div(id='qo_graphs'),
            html.H4(children="Sensor Gauges"),
            dcc.Dropdown(id='dropdown-gauge',
                         options=create_options(),
                         value=['FL_VSS'],
                         multi=True),
            html.Center(id='qo_gauges'),
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
                     figure=go.Figure(go.Scatter(x=data['Time'], y=data[sensor['id']])).update_layout(
                         title_text=sensor['label'] + " Graph",
                         xaxis=dict(rangeslider=dict(visible=True), type="linear")))


def create_graphs(sensors_lst, data):
    result = []
    for sensor in sensors_lst:
        result.append(create_header(sensors_lst[sensor]))
        result.append(create_graph(sensors_lst[sensor], data))
    return result


def create_grad_bar(sensor, data):
    curr = data[sensor['id']][len(data)-1]
    if curr > sensor['max_value'] or curr < sensor['min_value']:
        text_color='#FF0000'
    else:
        text_color='#4E2A84'
    return daq.LEDDisplay(id=sensor['id']+"_grad_bar",
                          label=sensor['label']+" ("+sensor['units']+")",
                          value=curr,
                          color=text_color,
                          style={'display': 'inline-block',
                                 'width': '20%'}
                          )


def create_grad_bars(data):
    result = []
    for i in range(len(all_sensors_lst)):
        #result.append(create_header(all_sensors_lst[i]))
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
    dash.dependencies.Output('qo_gauges', 'children'),

    dash.dependencies.Output('qo_graphs', 'children'),  # The graph on the quick overview tab
    dash.dependencies.Output('container-button-basic', 'children'),  # Updating the text under the button
    dash.dependencies.Output('qo_tab', 'children'), # Updates the quick-overview tab
    dash.dependencies.Output('all_sensors_tab', 'children'),  # Updates the all-sensors tab
    dash.dependencies.Output('high_sensors_tab', 'children'),  # Updates the high priority sensors tab
    dash.dependencies.Output('medium_sensors_tab', 'children'),
    dash.dependencies.Output('low_sensors_tab', 'children'),
    dash.dependencies.Output('safety_sensors_tab', 'children'),
    [dash.dependencies.Input('dropdown-gauge', 'value'),  # determines which sensor will be on the gauge for the qo tab
     dash.dependencies.Input('dropdown-graph', 'value'),  # determines which sensor will be on the graph for the qo tab
     dash.dependencies.Input('interval-component', 'n_intervals'),  # allows the page to update according to the refresh rate
     dash.dependencies.Input('pause-button', 'n_clicks'),  # determines whether the graphs are updating or not
     dash.dependencies.Input('tabs', 'value')  # determines which tab the user is on
     ]
)
def update_front_page(id_gauges, id_graphs, n_intervals, n_clicks, active_tab):
    data = pd.read_csv(file)
    if data['Time'][len(data)-1] == variables.most_recent_time:
        variables.most_recent_time = variables.most_recent_time
        return no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update, no_update

        # remove this comment if you want the page to update ONLY when a
        # new piece of data is received, this can improve efficiency but if you switch tabs, it will take until the
        # next piece of data is received to load the tab
    else:
        variables.most_recent_time = data['Time'][len(data)-1]

    if active_tab == 'qo_tab':
        return create_quick_overview_tab(id_gauges, id_graphs, n_clicks, data)
    elif active_tab == 'all_sensors_tab':
        return create_all_sensors_tab(data, n_clicks)
    elif active_tab == 'high_sensors_tab':
        return create_high_sensors_tab(data, n_clicks)
    elif active_tab == 'medium_sensors_tab':
        return create_med_senors_tab(data, n_clicks)
    elif active_tab == 'low_sensors_tab':
        return create_low_sensors_tab(data, n_clicks)
    elif active_tab == 'safety_sensors_tab':
        return create_safe_sensors_tab(data, n_clicks)
    else:
        raise PreventUpdate


def create_quick_overview_tab(id_gauges, id_graphs, n_clicks, data):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        graphs = []
        for id_graph in id_graphs:
            sensor_graph = find_sensor_given_id(id_graph)
            if sensor_graph:
                graphs.append(dcc.Graph(id=sensor_graph['id']+"_qo_graph",
                                        figure=go.Figure(go.Scatter(x=data['Time'][-300:], y=data[sensor_graph['id']][-300:])).update_layout(
                                            title_text=sensor_graph['label'] + " Graph",
                                            xaxis=dict(rangeslider=dict(visible=False), type="linear"))))
            else:
                raise PreventUpdate
    else:
        button = 'The live graphs are currently paused.'
        graphs = no_update

    gauges = []
    for id_gauge in id_gauges:
        sensor_gauge = find_sensor_given_id(id_gauge)
        if sensor_gauge:
            maxVal = sensor_gauge['max_value']
            minVal = sensor_gauge['min_value']
            gauge_unit = sensor_gauge['units']
            gauge_label = sensor_gauge['label']
            gauge_value = data[sensor_gauge['id']][len(data) - 1]
            gauges.append(daq.Gauge(id=sensor_gauge['id']+"_qo_gauge",
                                    max=maxVal,
                                    min=minVal,
                                    units=gauge_unit,
                                    label=gauge_label,
                                    value=gauge_value,
                                    showCurrentValue=True,
                                    style={'display': 'inline-block',
                                           'width': '20%'}))
        else:
            raise PreventUpdate

    return gauges, graphs, button, no_update, no_update, no_update, no_update, no_update, no_update


def create_sensor_tab(id_gauges, id_graphs, data, n_clicks, tab):
    if tab == 'qo_tab':
        return create_quick_overview_tab(id_gauges, id_graphs, n_clicks, data)
    elif tab == 'all_sensors_tab':
        return create_all_sensors_tab(data, n_clicks)
    elif tab == 'high_sensors_tab':
        return create_high_sensors_tab(data, n_clicks)
    elif tab == 'medium_sensors_tab':
        return create_med_senors_tab(data, n_clicks)
    elif tab == 'low_sensors_tab':
        return create_low_sensors_tab(data, n_clicks)
    elif tab == 'safety_sensors_tab':
        return create_safe_sensors_tab(data, n_clicks)


def create_all_sensors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
    else:
        button = 'The live graphs are currently paused.'
    all_children = create_grad_bars(data)
    return no_update, no_update, button, no_update, all_children, no_update, no_update, no_update, no_update


def create_high_sensors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        high_children = create_graphs(sensors.hp_sens, data)
    else:
        button = 'The live graphs are currently paused.'
        high_children = no_update
    return no_update, no_update, button, no_update, no_update, high_children, no_update, no_update, no_update


def create_med_senors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        medium_children = create_graphs(sensors.mp_sens, data)
    else:
        button = 'The live graphs are currently paused.'
        medium_children = no_update
    return no_update, no_update, button, no_update, no_update, no_update, medium_children, no_update, no_update


def create_low_sensors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        low_children = create_graphs(sensors.lp_sens, data)
    else:
        button = 'The live graphs are currently paused.'
        low_children = no_update
    return no_update, no_update, button, no_update, no_update, no_update, no_update, low_children, no_update


def create_safe_sensors_tab(data, n_clicks):
    if n_clicks % 2 == 1:
        button = 'The live graphs are currently being updated.'
        safety_children = create_graphs(sensors.s_sens, data)
    else:
        button = 'The live graphs are currently paused.'
        safety_children = no_update
    return no_update, no_update, button, no_update, no_update, no_update, no_update, no_update, safety_children

# Instead of graduated bars, do LED Displays, display in green if current value is greater than average of past 5 values
# Be able to select what you want on each axis, including time for the graphs


if __name__ == '__main__':
    app.run_server(debug=False)
